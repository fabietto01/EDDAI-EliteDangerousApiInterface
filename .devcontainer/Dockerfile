# ==============================================================================
# STAGE 1: upstream - Prepare Miniconda with conda environment
# ==============================================================================
FROM anaconda/miniconda:26.7.1 as upstream

# Set conda environment variables
ENV CONDA_HOME=/opt/miniconda3 \
    PATH=/opt/miniconda3/bin:$PATH \
    CONDA_PLUGINS_AUTO_ACCEPT_TOS=true

# Create and activate conda environment
COPY eddai_EliteDangerousApiInterface/environment-dev.yml* .devcontainer/noop.txt /tmp/conda-tmp/
RUN if [ -f "/tmp/conda-tmp/environment-dev.yml" ]; then \
        umask 0002 && /opt/miniconda3/bin/conda env update -n base -f /tmp/conda-tmp/environment-dev.yml; \
    fi && \
    rm -rf /tmp/conda-tmp

# ==============================================================================
# STAGE 2: production - Final optimized image with VS Code DevContainer base
# ==============================================================================
FROM mcr.microsoft.com/devcontainers/base:dev-debian

ARG USERNAME=vscode

# Setup conda from upstream stage
ENV CONDA_HOME=/opt/miniconda3 \
    PATH=/opt/miniconda3/bin:$PATH \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# Copy conda installation from upstream stage
COPY --chown=${USERNAME}:${USERNAME} --from=upstream /opt/miniconda3 /opt/miniconda3

# Create conda symlink for standard conda location
RUN ln -s /opt/miniconda3/etc/profile.d/conda.sh /etc/profile.d/conda.sh \
    && echo ". /opt/miniconda3/etc/profile.d/conda.sh" >> /home/${USERNAME}/.bashrc \
    && echo "conda activate base" >> /home/${USERNAME}/.bashrc

# Install additional runtime dependencies for conda and development tools
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y --no-install-recommends \
        bzip2 \
        build-essential \
        ca-certificates \
        curl \
        git \
        iproute2 \
        libglib2.0-0 \
        libsm6 \
        libxcomposite1 \
        libxcursor1 \
        libxdamage1 \
        libxext6 \
        libxfixes3 \
        libxi6 \
        libxinerama1 \
        libxrandr2 \
        libxrender1 \
        nodejs \
        npm \
        openssh-client \
        procps \
        sudo \
        wget \
    && apt-get upgrade -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# ============================================================================== 
# SECURITY & PERMISSIONS SETUP
# ==============================================================================

# Ensure conda is executable by the user
RUN chown -R ${USERNAME}:${USERNAME} /opt/miniconda3

# Fix workspaces ownership and permissions
RUN mkdir -p /workspaces && \
    chown -R ${USERNAME}:${USERNAME} /workspaces && \
    chmod -R u+rwx /workspaces

# Fix home directory permissions (critical for SSH, git, npm)
RUN chown -R ${USERNAME}:${USERNAME} /home/${USERNAME} && \
    chmod 700 /home/${USERNAME}/.ssh 2>/dev/null || true && \
    chmod 644 /home/${USERNAME}/.ssh/authorized_keys 2>/dev/null || true

# Configure git security for the user (trust workspace directory)
RUN git config --global --add safe.directory /workspaces && \
    git config --global --add safe.directory /workspaces/EDDAI-EliteDangerousApiInterface && \
    git config --global init.defaultBranch main

# Ensure user can access /tmp and /var directories
RUN chown -R ${USERNAME}:${USERNAME} /tmp && \
    chmod 1777 /tmp

# Fix conda and npm cache directories permissions
RUN mkdir -p /home/${USERNAME}/.npm /home/${USERNAME}/.conda && \
    chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}/.npm /home/${USERNAME}/.conda

# Create .bashrc customizations for better development experience
RUN echo "" >> /home/${USERNAME}/.bashrc && \
    echo "# Enhanced development environment" >> /home/${USERNAME}/.bashrc && \
    echo "export PYTHONUNBUFFERED=1" >> /home/${USERNAME}/.bashrc && \
    echo "export NODE_ENV=development" >> /home/${USERNAME}/.bashrc && \
    echo "alias ll='ls -lah'" >> /home/${USERNAME}/.bashrc && \
    echo "alias python='python3'" >> /home/${USERNAME}/.bashrc

# Set proper ownership of the final user shell configuration
RUN chown ${USERNAME}:${USERNAME} /home/${USERNAME}/.bashrc /home/${USERNAME}/.profile

# Verify permissions are correct
RUN echo "=== Permission Verification ===" && \
    echo "User: $(id ${USERNAME})" && \
    echo "Workspaces ownership:" && ls -ld /workspaces && \
    echo "Home ownership:" && ls -ld /home/${USERNAME} && \
    echo "=== Setup Complete ==="