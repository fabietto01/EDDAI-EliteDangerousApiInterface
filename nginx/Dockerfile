# ==============================================
# STAGE 1: Frontend build - compile Vue.js SPA
# ==============================================
FROM node:22-alpine AS frontend-builder

WORKDIR /app

# Copy package files first to leverage layer caching
COPY eddai_EliteDangerousApiInterface/ed_frontend/package*.json ./ed_frontend/

WORKDIR /app/ed_frontend

# Install all deps (including devDeps: vite is needed for the build)
RUN npm ci

# Copy source after deps to avoid cache invalidation on code changes
COPY eddai_EliteDangerousApiInterface/ed_frontend/ ./

# vite outDir "../static-server/vuejs/" resolves to /app/static-server/vuejs/
RUN npm run build

# ==============================================
# STAGE 2: Production nginx with baked statics
# ==============================================
FROM nginx:1.25-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx/nginx.conf /etc/nginx/conf.d/

# Bake the compiled Vue.js bundle into the image at a dedicated path.
# In K8s: mount an emptyDir at /app/django-static/ (populated by an
# initContainer running "collectstatic") without touching this path.
COPY --from=frontend-builder /app/static-server/vuejs/ /app/vuejs/

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget -qO- http://localhost/health || exit 1
