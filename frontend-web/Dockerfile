FROM node:18-alpine

WORKDIR /app

# Build argument com valor padrão (funciona mesmo sem Build Args no Easypanel)
ARG NEXT_PUBLIC_API_URL=https://hdt-energy-facial.mqtl34.easypanel.host/api/v1
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

# Copiar package files
COPY package.json package-lock.json ./

# Instalar dependências
RUN npm ci

# Copiar arquivos de configuração
COPY next.config.js ./
COPY tsconfig.json ./
COPY tailwind.config.ts* ./
COPY postcss.config.js* ./

# Copiar source code
COPY src ./src

# Build (variável disponível aqui!)
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

# Expor porta
EXPOSE 3000

# Start
ENV NODE_ENV=production
CMD ["npm", "start"]
