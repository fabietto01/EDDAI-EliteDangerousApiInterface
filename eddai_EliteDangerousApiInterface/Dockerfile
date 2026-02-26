# ============================================
# STAGE 1: Frontend Builder - Build Vue.js app
# ============================================
FROM node:20-slim AS frontend-builder

WORKDIR /build

# Copy package files first for better layer caching
COPY ./ed_frontend/package.json ./ed_frontend/package-lock.json* ./

# Install dependencies (ci for reproducible builds)
RUN npm ci --ignore-scripts

# Copy Vue.js source code
COPY ./ed_frontend/ ./

# Build for production
ENV NODE_ENV=production
RUN npm run build

# ============================================
# STAGE 2: Backend Builder - Install conda env
# ============================================
FROM continuumio/miniconda3:25.3.1-1 AS backend-builder

# Configure PROJ_LIB environment variable for GDAL
ENV PROJ_LIB=/opt/conda/share/proj

# Set working directory for build
WORKDIR /tmp/build

# Copy and install conda environment
COPY ./environment.yml .
RUN umask 0002 && \
    /opt/conda/bin/conda env update -n base -f environment.yml && \
    # Install PROJ data if needed
    if [ ! -d "/opt/conda/share/proj" ]; then \
        conda install -y -c conda-forge proj-data; \
    fi && \
    # Clean conda cache and unnecessary files
    conda clean -afy && \
    # Remove static libraries (not needed at runtime)
    find /opt/conda -follow -type f -name '*.a' -delete && \
    # Remove Python cache
    find /opt/conda -follow -type f -name '*.pyc' -delete && \
    find /opt/conda -follow -type f -name '*.pyo' -delete && \
    # Remove JavaScript source maps
    find /opt/conda -follow -type f -name '*.js.map' -delete && \
    # Remove conda package cache
    rm -rf /opt/conda/pkgs

# ============================================
# STAGE 3: Runtime - Final lightweight image
# ============================================
FROM continuumio/miniconda3:25.3.1-1

# Set environment variables
ENV APP_HOME=/app
ENV PROJ_LIB=/opt/conda/share/proj

# Copy ONLY the compiled conda environment from builder (without cache/temp files)
COPY --from=backend-builder /opt/conda /opt/conda

# Create app directory and set working directory
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

# Copy application code (respects .dockerignore)
COPY . $APP_HOME

# Copy Vue.js built assets into the static/ directory (part of STATICFILES_DIRS)
# collectstatic will then copy them to STATIC_ROOT (static-server/)
COPY --from=frontend-builder /static/vuejs/ $APP_HOME/static/vuejs/

# Create system user, set permissions, and cleanup in a single layer
RUN addgroup --system app && \
    adduser --system --group app && \
    chown -R app:app $APP_HOME && \
    chmod +x $APP_HOME/entrypoint.sh && \
    mkdir -p /opt/conda/share/proj && \
    chmod -R 755 /opt/conda/share/proj && \
    # Remove any Python cache that might have been copied
    find $APP_HOME -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true && \
    find $APP_HOME -type f -name "*.pyc" -delete 2>/dev/null || true

# Switch to non-root user
USER app

ENTRYPOINT ["./entrypoint.sh"]