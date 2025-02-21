FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Set non-interactive mode for apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set Python3 as default
RUN ln -s /usr/bin/python3 /usr/bin/python

# Upgrade pip
RUN python -m pip install --upgrade pip

# Setup Python env
COPY Pipfile ./
COPY Pipfile.lock ./
RUN pip install pipenv
RUN pipenv sync

# Default command
CMD ["/bin/bash"]


