#!/bin/bash

# Path to the input file
input_file="message.txt"

# Path to the output directory
output_dir="/storage/plzen4-ntis/home/dcifka20/output/"

# Path to the synthesize.py script
synthesize_script="/storage/plzen4-ntis/home/dcifka20/GIT_repos/Coqui-TTS/TTS/bin/synthesize.py"

# Model path
model_path="/storage/plzen4-ntis/home/dcifka20/hds/models/VITS4_MyVoice.ft-SPT-MGW-m10f10.ph-redu.p2b0.ddp.kl5/checkpoint_92001-999.pth"

# Config path
config_path="/storage/plzen4-ntis/home/dcifka20/hds/models/VITS4_MyVoice.ft-SPT-MGW-m10f10.ph-redu.p2b0.ddp.kl5/config.json"

# Create output directory if it doesn't exist
mkdir -p "$output_dir"

# Iterate over each line in the input file
index=0
while IFS= read -r line; do
    # Increment index
    ((index++))
    
    # Text from the current line
    text="$line"
    
    # Output path
    out_path="$output_dir$index.wav"
    
    # Call synthesize.py with the appropriate arguments
    python3 "$synthesize_script" \
        --model_path="$model_path" \
        --config_path="$config_path" \
        --text="$text" \
        --out_path="$out_path"
done < "$input_file"