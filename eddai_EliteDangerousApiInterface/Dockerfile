# ============================================
# STAGE 1: Builder - Install all dependencies
# ============================================
FROM anaconda/miniconda:26.7.1 AS builder

# Configure PROJ_LIB environment variable for GDAL
ENV CONDA_HOME=/opt/miniconda3 \
    PATH=/opt/miniconda3/bin:$PATH \
    CONDA_PLUGINS_AUTO_ACCEPT_TOS=true \
    PROJ_LIB=/opt/eddai/share/proj

# Set working directory for build
WORKDIR /tmp/build

# Copy and install conda environment
COPY ./environment.yml .
RUN umask 0002 && \
    /opt/miniconda3/bin/conda env create --prefix /opt/eddai -f environment.yml && \
    # Install PROJ data if needed
    if [ ! -d "/opt/eddai/share/proj" ]; then \
        /opt/miniconda3/bin/conda install --prefix /opt/eddai -y -c conda-forge proj-data; \
    fi && \
    # Clean conda cache and unnecessary files
    /opt/miniconda3/bin/conda clean -afy && \
    # Remove static libraries (not needed at runtime)
    find /opt/eddai -follow -type f -name '*.a' -delete && \
    # Remove Python cache
    find /opt/eddai -follow -type f -name '*.pyc' -delete && \
    find /opt/eddai -follow -type f -name '*.pyo' -delete && \
    # Remove JavaScript source maps
    find /opt/eddai -follow -type f -name '*.js.map' -delete

# ============================================
# STAGE 2: Runtime - Final lightweight image
# ============================================
FROM debian:trixie-slim AS runtime

# Set environment variables
ENV APP_HOME=/app \
    APP_ENV=/opt/eddai \
    PATH=/opt/eddai/bin:$PATH \
    PROJ_LIB=/opt/eddai/share/proj

# Install only the runtime tools required by the entrypoint and user setup
RUN apt-get update && \
    apt-get install -y --no-install-recommends bash passwd && \
    rm -rf /var/lib/apt/lists/*

# Copy only the application environment, not the Conda installation
COPY --from=builder /opt/eddai /opt/eddai

# Create app directory and set working directory
RUN mkdir -p $APP_HOME/static-server $APP_HOME/media-server
WORKDIR $APP_HOME

# Copy application code (respects .dockerignore)
COPY . $APP_HOME

# Create system user, set permissions, and cleanup in a single layer
RUN groupadd --system app && \
    useradd --system --gid app --no-create-home app && \
    chown -R app:app $APP_HOME && \
    sed -i 's/\r$//' $APP_HOME/entrypoint.sh && \
    chmod +x $APP_HOME/entrypoint.sh && \
    chmod -R 755 /opt/eddai/share/proj && \
    # Remove any Python cache that might have been copied
    find $APP_HOME -type d -name __pycache__ -exec rm -rf {} + && \
    find $APP_HOME -type f -name "*.pyc" -delete

# Switch to non-root user
USER app

EXPOSE 8080
ENTRYPOINT ["./entrypoint.sh"]