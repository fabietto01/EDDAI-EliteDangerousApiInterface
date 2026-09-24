# syntax=docker/dockerfile:1

# Immagine backend gia' pubblicata da cui copiare gli asset Django raccolti con collectstatic.
ARG BACKEND_IMAGE=ghcr.io/fabietto01/eddai-elitedangerousapiinterface:latest
FROM ${BACKEND_IMAGE} AS backend-static

# ============================================
# STAGE 1: Dipendenze Node
# ============================================
FROM node:24-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

# ============================================
# STAGE 2: Build Vue (Vite)
# ============================================
FROM deps AS build
ARG APP_VERSION=dev
ARG GIT_SHA=unknown
ENV APP_VERSION=${APP_VERSION} \
    GIT_SHA=${GIT_SHA} \
    NODE_ENV=production
COPY . .
RUN npm run build

# ============================================
# STAGE 3: Runtime Nginx non-root
# ============================================
FROM nginxinc/nginx-unprivileged:1.27-alpine-slim AS runtime
USER root

RUN rm -f /etc/nginx/conf.d/default.conf

COPY docker/nginx.conf /etc/nginx/nginx.conf
COPY docker/snippets/ /etc/nginx/snippets/
COPY docker/conf.d/default.conf.template /etc/nginx/templates/default.conf.template
COPY --from=build /app/dist /usr/share/nginx/html
COPY --from=backend-static /app/static-server /usr/share/nginx/django-static

RUN mkdir -p /usr/share/nginx/media && \
    chown -R nginx:nginx /usr/share/nginx/html /usr/share/nginx/django-static /usr/share/nginx/media

ENV DJANGO_UPSTREAM_HOST=django \
    DJANGO_UPSTREAM_PORT=8080

USER nginx

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget -q -O- --spider http://127.0.0.1:8080/healthz || exit 1
