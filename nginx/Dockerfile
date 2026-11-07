FROM node:24-alpine AS frontend-build

WORKDIR /app/ed_frontend
COPY eddai_EliteDangerousApiInterface/ed_frontend/package.json eddai_EliteDangerousApiInterface/ed_frontend/package-lock.json ./
RUN npm ci
COPY eddai_EliteDangerousApiInterface/ed_frontend/ ./
RUN npm run build

FROM nginx/nginx-unprivileged:1.31.8-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=frontend-build /app/ed_frontend/dist/ /usr/share/nginx/html/

USER 101
EXPOSE 8080