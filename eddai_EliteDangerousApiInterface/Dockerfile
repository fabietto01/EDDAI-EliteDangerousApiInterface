# ============================================
# STAGE 1: Builder - Install all dependencies
# ============================================
FROM anaconda/miniconda:26.7.1 AS builder

# Configure PROJ_LIB environment variable for GDAL
ENV CONDA_HOME=/opt/miniconda3 \
    PATH=/opt/miniconda3/bin:$PATH \
    CONDA_PLUGINS_AUTO_ACCEPT_TOS=true \
    PROJ_LIB=/opt/miniconda3/share/proj

# Set working directory for build
WORKDIR /tmp/build

# Copy and install conda environment
COPY ./environment.yml .
RUN umask 0002 && \
    /opt/miniconda3/bin/conda env update -n base -f environment.yml && \
    # Install PROJ data if needed
    if [ ! -d "/opt/miniconda3/share/proj" ]; then \
        /opt/miniconda3/bin/conda install -y -c conda-forge proj-data; \
    fi && \
    # Clean conda cache and unnecessary files
    /opt/miniconda3/bin/conda clean -afy && \
    # Remove static libraries (not needed at runtime)
    find /opt/miniconda3 -follow -type f -name '*.a' -delete && \
    # Remove Python cache
    find /opt/miniconda3 -follow -type f -name '*.pyc' -delete && \
    find /opt/miniconda3 -follow -type f -name '*.pyo' -delete && \
    # Remove JavaScript source maps
    find /opt/miniconda3 -follow -type f -name '*.js.map' -delete && \
    # Remove conda package cache
    rm -rf /opt/miniconda3/pkgs

# ============================================
# STAGE 2: Runtime - Final lightweight image
# ============================================
FROM anaconda/miniconda:26.7.1

# Set environment variables
ENV APP_HOME=/app
ENV CONDA_HOME=/opt/miniconda3 \
    PATH=/opt/miniconda3/bin:$PATH \
    PROJ_LIB=/opt/miniconda3/share/proj

# Copy ONLY the compiled conda environment from builder (without cache/temp files)
COPY --from=builder /opt/miniconda3 /opt/miniconda3

# Create app directory and set working directory
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# Copy application code (respects .dockerignore)
COPY . $APP_HOME

# Raccoglie gli asset statici (admin, DRF, Swagger, ReDoc) nell'immagine: nessuna
# connessione al DB e' richiesta da collectstatic, i valori sotto sono solo placeholder di build.
RUN DJANGO_SECRET_KEY=build-time-placeholder-not-a-secret \
    DJANGO_SETTINGS_MODULE=eddai_EliteDangerousApiInterface.settings.prod \
    python manage.py collectstatic --noinput

# Create system user, set permissions, and cleanup in a single layer
RUN groupadd --system app && \
    useradd --system --gid app --no-create-home app && \
    chown -R app:app $APP_HOME && \
    # Normalizza gli EOL: un entrypoint con CRLF (checkout Windows) fallisce con "no such file or directory"
    sed -i 's/\r$//' $APP_HOME/entrypoint.sh && \
    chmod +x $APP_HOME/entrypoint.sh && \
    mkdir -p /opt/miniconda3/share/proj && \
    chmod -R 755 /opt/miniconda3/share/proj && \
    # Remove any Python cache that might have been copied
    find $APP_HOME -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true && \
    find $APP_HOME -type f -name "*.pyc" -delete 2>/dev/null || true

# Switch to non-root user
USER app

ENTRYPOINT ["./entrypoint.sh"]