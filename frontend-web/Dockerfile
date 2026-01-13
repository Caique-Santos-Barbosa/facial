FROM node:18-alpine

WORKDIR /app

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

# Build
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

# Expor porta
EXPOSE 3000

# Start
ENV NODE_ENV=production
CMD ["npm", "start"]
