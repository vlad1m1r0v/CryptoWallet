# Етап 1: Збірка (Build)
FROM node:20-alpine AS builder

WORKDIR /app

# Копіюємо файли залежностей
COPY package*.json ./
RUN npm install

# Копіюємо весь код і збираємо проект
COPY . .
RUN npm run build

# Етап 2: Запуск (Runner)
FROM node:20-alpine AS runner

WORKDIR /app

# Копіюємо тільки результат збірки та package.json
COPY --from=builder /app/build ./build
COPY --from=builder /app/package*.json ./

# Встановлюємо лише production залежності
RUN npm ci --omit=dev

# SvelteKit adapter-node за замовчуванням слухає порт 3000
ENV PORT=3000
EXPOSE 3000

# Запуск сервера
CMD ["node", "build"]