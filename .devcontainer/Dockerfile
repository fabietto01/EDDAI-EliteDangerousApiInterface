# Development image with the current official Miniconda base
FROM anaconda/miniconda:26.7.1

ENV CONDA_HOME=/opt/miniconda3 \
    PATH=/opt/miniconda3/bin:$PATH \
    CONDA_PLUGINS_AUTO_ACCEPT_TOS=true

# Create and activate conda environment
COPY eddai_EliteDangerousApiInterface/environment-dev.yml* .devcontainer/noop.txt /tmp/conda-tmp/
RUN if [ -f "/tmp/conda-tmp/environment-dev.yml" ]; then \
        umask 0002 && /opt/miniconda3/bin/conda env update -n base -f /tmp/conda-tmp/environment-dev.yml; \
    fi && \
    rm -rf /tmp/conda-tmp

# Tools used by VS Code Dev Containers, Git, debugging, and frontend development.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        git \
        iproute2 \
        nodejs \
        npm \
        procps \
        sudo \
        wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*