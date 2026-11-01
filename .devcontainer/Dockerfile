# Install the project environment before copying it into the VS Code image.
FROM anaconda/miniconda:26.7.1 AS conda

ENV CONDA_HOME=/opt/miniconda3 \
    PATH=/opt/miniconda3/bin:$PATH \
    CONDA_PLUGINS_AUTO_ACCEPT_TOS=true

COPY eddai_EliteDangerousApiInterface/environment-dev.yml* .devcontainer/noop.txt /tmp/conda-tmp/
RUN if [ -f "/tmp/conda-tmp/environment-dev.yml" ]; then \
        umask 0002 && /opt/miniconda3/bin/conda env update -n base -f /tmp/conda-tmp/environment-dev.yml; \
    fi && \
    rm -rf /tmp/conda-tmp
RUN /opt/miniconda3/bin/conda remove -n base -y conda-anaconda-telemetry

# Provide Node.js and npm without pulling the large Debian npm dependency tree.
FROM node:24-bookworm-slim AS node

# Keep the VS Code Dev Containers base and its vscode user in the final image.
FROM mcr.microsoft.com/devcontainers/base:dev-debian

ARG USERNAME=vscode

ENV CONDA_HOME=/opt/miniconda3 \
    PATH=/opt/miniconda3/bin:$PATH \
    CONDA_PLUGINS_AUTO_ACCEPT_TOS=true \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

COPY --chown=${USERNAME}:${USERNAME} --from=conda /opt/miniconda3 /opt/miniconda3
COPY --from=node /usr/local/ /usr/local/

RUN ln -sfn /opt/miniconda3/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/miniconda3/etc/profile.d/conda.sh" >> /home/${USERNAME}/.bashrc && \
    echo "conda activate base" >> /home/${USERNAME}/.bashrc

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y --no-install-recommends \
        bzip2 \
        build-essential \
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
        openssh-client \
        procps \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

USER ${USERNAME}