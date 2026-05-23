# ============================================
# STAGE 1: Builder - Build Vue app with Vite
# ============================================
FROM node:22-alpine3.22 AS builder

WORKDIR /app

# Copy package files first to leverage Docker layer cache
COPY package*.json ./

# Install all dependencies (devDependencies required for Vite build)
RUN npm ci && npm cache clean --force

# Copy application source (respects .dockerignore)
COPY . .

# Build with root base path and standard output dir for Docker.
# Overrides vite.config.js defaults, which target Django's static folder.
RUN npm run build -- --base / --outDir dist

# ============================================
# STAGE 2: Runtime - Serve SPA with nginx
# ============================================
FROM nginx:1.27-alpine3.22

# Remove default nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built Vue SPA from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget -qO- http://localhost/ || exit 1
