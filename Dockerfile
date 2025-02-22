FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

ENV PATH="/app/.venv/bin:$PATH"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Setup Python env
RUN mkdir /app
COPY pyproject.toml uv.lock .python-version /app
WORKDIR /app
RUN uv sync --frozen --no-cache

# Default command
CMD ["/bin/bash"]
