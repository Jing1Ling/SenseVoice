
# Use the specified base image
FROM vault.habana.ai/gaudi-docker/1.21.3/ubuntu22.04/habanalabs/pytorch-installer-2.6.0:latest


# Proxy support (only set if provided)
ARG http_proxy
ARG https_proxy
ARG no_proxy
ENV http_proxy=${http_proxy}
ENV https_proxy=${https_proxy}
ENV no_proxy=${no_proxy}

# Set environment variables
ENV PATH=/root/.local/bin:${PATH}
ENV HF_ENDPOINT=https://hf-mirror.com
ENV PT_HPU_LAZY_MODE=0

# Update system packages and install Git, Git LFS, FFmpeg, curl
RUN apt-get update && apt-get install -y \
    git \
    git-lfs \
    ffmpeg \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Initialize Git LFS
RUN git lfs install

# git user config
RUN git config --global user.name "Examples"
RUN git config --global user.email "examples@intel.com"

# Set the working directory
WORKDIR /workspace

# Copy all files from local patches directory to /workspace/patches, overwriting existing files
# This ensures /workspace/patches contains the latest patches from the build context
COPY patches/. /workspace/patches/

# Clone SenseVoice repository
ARG SV_REPO=https://github.com/FunAudioLLM/SenseVoice.git
ARG SV_COMMIT=4462e356e2d655bbe8354b7e0f01309d13ca6e4d
ARG SV_PATCHES_DIR=/workspace/patches
RUN git clone $SV_REPO
WORKDIR /workspace/SenseVoice
RUN git checkout $SV_COMMIT \
    && git submodule update --init --recursive \
    && git am $SV_PATCHES_DIR/* || true

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt || true

# Default command (can be modified as needed)
CMD ["/bin/bash"]
