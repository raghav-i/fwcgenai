#!/bin/bash

# Install Mambaforge
wget https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh
bash Mambaforge-Linux-x86_64.sh -b -f -p /usr/local
export PATH=/usr/local/bin/:$PATH

# Create a conda environment and activate it
mamba create -n myenv python=3.8 -y
source activate myenv

# Install required packages
pip install opencv-python torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118
pip install timm einops albumentations matplotlib tensorboard jax accelerate
pip install diffusers ftfy madgrad openai-clip numpy transformers
pip install flask pyngrok

