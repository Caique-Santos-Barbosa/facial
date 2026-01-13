FROM node:18-alpine

WORKDIR /app

# Argumentos de build (para variáveis NEXT_PUBLIC_*)
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

# Copiar package files
COPY package*.json ./

# Instalar dependências
RUN npm ci

# Copiar arquivos de configuração
COPY next.config.js ./
COPY tsconfig.json ./
COPY tailwind.config.ts* ./
COPY postcss.config.js* ./

# Copiar source code
COPY src ./src

# Build (as variáveis NEXT_PUBLIC_* são injetadas aqui)
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

# Expor porta
EXPOSE 3000

# Start
ENV NODE_ENV=production
CMD ["npm", "start"]
