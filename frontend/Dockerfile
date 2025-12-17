# Етап 1: Збірка (Builder)
FROM node:20-alpine AS builder

WORKDIR /app

# Оголошуємо аргументи збірки (Easypanel передасть їх сюди)
ARG PUBLIC_BACKEND_URL
ARG PUBLIC_SOCKET_URL
ARG PUBLIC_CHAT_URL

# Робимо ці аргументи доступними як змінні оточення для процесу збірки
ENV PUBLIC_BACKEND_URL=$PUBLIC_BACKEND_URL
ENV PUBLIC_SOCKET_URL=$PUBLIC_SOCKET_URL
ENV PUBLIC_CHAT_URL=$PUBLIC_CHAT_URL

COPY package*.json ./
RUN npm install

COPY . .
# Тепер Vite побачить ці змінні і не буде падати
RUN npm run build

# Етап 2: Запуск (Runner)
FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/build ./build
COPY --from=builder /app/package*.json ./
RUN npm ci --omit=dev
ENV PORT=3000
EXPOSE 3000
CMD ["node", "build"]