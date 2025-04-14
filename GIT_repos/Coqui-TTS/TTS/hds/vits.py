
from typing import Dict,Tuple,List

import numpy as np
import torch
from torch import nn
from torch.cuda.amp.autocast_mode import autocast

from coqpit import Coqpit

from TTS.tts.models.vits import Vits,wav_to_mel
from TTS.tts.utils.helpers import segment, sequence_mask
from TTS.tts.utils.text.tokenizer import TTSTokenizer
from TTS.utils.audio.processor import AudioProcessor

class VitsHDS(Vits):


    # --------------
    def __init__(self, config:Coqpit, ap:AudioProcessor = None, tokenizer:TTSTokenizer = None, **kws):
        """ Custom VITS constructor. Add additional parameters as required.
        """
        super().__init__(config, ap = ap, tokenizer = tokenizer)

    # --------------
    def train_step(self, batch: dict, criterion: List[str], optimizer_idx: int) -> Tuple[Dict, Dict]:
        """Perform a single training step. Run the model forward pass and compute losses.

        Args:
            batch (Dict): Input tensors.
            criterion (List): Loss layer designed for the model.
            optimizer_idx (int): Index of optimizer to use. 0 for the generator and 1 for the discriminator networks.

        Returns:
            Tuple[Dict, Dict]: Model outputs and computed losses.
        """


        # Discriminator
        if optimizer_idx == 0 :
            
            print('Volám diskriminátor pro výpočet loss funkce')

            # Synthesize
            # NOTE: may be cached for the future use
            outputs = self.forward(batch["tokens"], batch["token_lens"], batch["spec"], batch["spec_lens"], batch["waveform"])

            # Generated and real speech segments
            speech_gener = outputs['model_outputs']
            speech_real  = outputs['waveform_seg']

            # Use discriminator
            # Detach the generated speech, as we do not want update weights of the generator
            scores_disc_fake,_,scores_disc_real,_ = self.disc(speech_gener.detach(), speech_real)

           # Výpočet diskriminator loss funkce
            return_dict = {}
            loss = 0.0
            loss_disc, loss_disc_real, _ = self.discriminator_loss(scores_real=scores_disc_real, scores_fake=scores_disc_fake)
            return_dict["loss_disc"] = loss_disc * self.config.disc_loss_alpha
            loss = loss + return_dict["loss_disc"]
            return_dict["loss"] = loss

            #Ulozeni jednotlivych diskriminačních loss hodnot
            for i, ldr in enumerate(loss_disc_real):
                return_dict[f"loss_disc_real_{i}"] = ldr
            return (outputs, return_dict)



        # Generator
        else :
            
            print('Volám generátor pro výpočet loss funkcí.')

            # Synthesize
            outputs = self.forward(batch["tokens"], batch["token_lens"], batch["spec"], batch["spec_lens"], batch["waveform"])

            # Generated and real speech segments
            speech_gener = outputs['model_outputs']
            speech_real  = outputs['waveform_seg']

            scores_disc_fake,_,scores_disc_real,_ = self.disc(speech_gener.detach(), speech_real)

            loss = 0.0
            return_dict = {}
            z_mask = sequence_mask(batch["spec_lens"]).float()
            
            # výpočet KL loss
            loss_kl = (
                self.kl_loss(z_p=outputs['z_p'], logs_q=outputs['logs_q'], m_p=outputs['m_p'], logs_p=outputs['logs_p'], z_mask=z_mask.unsqueeze(1))
                * self.config.kl_loss_alpha
            )
            
            # Výpočet příznakové loss funkce
            loss_feat = (
                self.feature_loss(feats_real=scores_disc_real, feats_generated=scores_disc_fake) * self.config.feat_loss_alpha
            )
            
            # Výpočet generator loss
            loss_gen = self.generator_loss(scores_fake=scores_disc_fake)[0] * self.config.gen_loss_alpha
            
            # Výpočet mel loss
            mel = segment(batch["mel"].float(), outputs["slice_ids"], self.spec_segment_size, pad_short=True)
            out_pred_seg = segment(outputs["model_outputs"].float(), outputs["slice_ids"], self.spec_segment_size, pad_short=True)
            loss_mel = self.mel_loss(mel, out_pred_seg) * self.config.mel_loss_alpha

            loss_dur = self.duration_loss(output["dur"], output["token_emb"], output["token_mask"]) * self.config.dur_loss_alpha
            loss = loss_kl + loss_feat + loss_mel + loss_gen + loss_dur

            #Slovník výsledků pro jednotlivé loss funkce a celkovou loss.
            return_dict["loss_gen"] = loss_gen
            return_dict["loss_kl"] = loss_kl
            return_dict["loss_feat"] = loss_feat
            return_dict["loss_mel"] = loss_mel
            return_dict["loss_dur"] = loss_dur
            return_dict["loss"] = loss
            return (outputs, return_dict)



    # --------------
    @staticmethod
    def discriminator_loss(scores_real, scores_fake):
        loss = 0
        real_losses = []
        fake_losses = []
        for dr, dg in zip(scores_real, scores_fake):
            dr = dr.float()
            dg = dg.float()
            real_loss = torch.mean((1 - dr) ** 2)
            fake_loss = torch.mean(dg**2)
            loss += real_loss + fake_loss
            real_losses.append(real_loss.item())
            fake_losses.append(fake_loss.item())
        return loss, real_losses, fake_losses

    # --------------
    @staticmethod
    def feature_loss(feats_real, feats_generated):
        loss = 0
        for dr, dg in zip(feats_real, feats_generated):
            for rl, gl in zip(dr, dg):
                rl = rl.float().detach()
                gl = gl.float()
                loss += torch.mean(torch.abs(rl - gl))
        return loss * 2

    @staticmethod
    def generator_loss(scores_fake):
        loss = 0
        gen_losses = []
        for dg in scores_fake:
            dg = dg.float()
            l = torch.mean((1 - dg) ** 2)
            gen_losses.append(l)
            loss += l

        return loss, gen_losses


    @staticmethod
    def duration_loss(self, dur, x, x_mask):
        durations = torch.log(dur + 1e-6) * x_mask
        durations_pred = self.duration_predictor(x, x_mask)

        loss = torch.sum((durations_pred - durations)** 2 [1, 2] ) / torch.sum(x_mask)
        loss = torch.sum(loss)

        return loss

    @staticmethod
    def kl_loss(z_p, logs_q, m_p, logs_p, z_mask):
        """
        z_p, logs_q: [b, h, t_t]
        m_p, logs_p: [b, h, t_t]
        """
        z_p = z_p.float()
        logs_q = logs_q.float()
        m_p = m_p.float()
        logs_p = logs_p.float()
        z_mask = z_mask.float()

        kl = logs_p - logs_q - 0.5
        kl += 0.5 * ((z_p - m_p) ** 2) * torch.exp(-2.0 * logs_p)
        kl = torch.sum(kl * z_mask)
        l = kl / torch.sum(z_mask)
        return l

    def mel_loss(self, mel_gt, out_pred):
        mel_pred = wav_to_mel(
            y=out_pred,
            n_fft=self.config.audio.fft_size,
            sample_rate=self.config.audio.sample_rate,
            num_mels=self.config.audio.num_mels,
            hop_length=self.config.audio.hop_length,
            win_length=self.config.audio.win_length,
            fmin=self.config.audio.mel_fmin,
            fmax=self.config.audio.mel_fmax,
            center=False,
        )

        l1 = torch.nn.functional.l1_loss
        return l1(mel_gt, mel_pred)

