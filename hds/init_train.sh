#!/bin/bash

# Make dirs
mkdir bin configs datasets models notebooks output_logs output_notebooks output_wavs tensorboard tmp_files test_files

cat > .gitignore <<EOL
# Model files
*.pth
*.pth.tar
*.out.*.ipynb
ipykernel_launcher.py
trainer_*_log.txt
output_notebooks/
tmp_files/

# Tensorboard
tensorboard/
events.out.*

.ipynb_checkpoints/
JupyterLabJob.e*
JupyterLabJob.o*

# Media files
*.wav
*.png
EOL
