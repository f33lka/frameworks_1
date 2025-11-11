# syntax=docker/dockerfile:1
########################
# 1) Build (Vite/React)
########################
FROM node:20-alpine AS builder
WORKDIR /app

# Устанавливаем зависимости
COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./
RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi

# Копируем исходники и билдим
COPY . .

# ENV для Vite (считывается на этапе сборки)
ARG VITE_API_URL=/api
ENV VITE_API_URL=${VITE_API_URL}

RUN npm run build

########################
# 2) Runtime (Nginx)
########################
FROM nginx:1.27-alpine

# Конфиг с проксированием /api -> backend:5000
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

# Готовый фронтенд
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

HEALTHCHECK --interval=15s --timeout=3s --start-period=10s --retries=5 \
  CMD wget -qO- http://127.0.0.1/ >/dev/null 2>&1 || exit 1
