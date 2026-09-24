FROM node:22-alpine AS build
WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:1.27-alpine AS runner
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /static-server/vuejs /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
