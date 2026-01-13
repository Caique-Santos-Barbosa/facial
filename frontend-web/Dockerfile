FROM node:18-alpine AS base

# Dependências apenas
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Copiar APENAS package.json e package-lock.json
COPY package.json package-lock.json* ./
RUN npm ci

# Builder
FROM base AS builder
WORKDIR /app

# Copiar node_modules do estágio anterior
COPY --from=deps /app/node_modules ./node_modules

# Copiar APENAS arquivos do frontend
COPY package.json package-lock.json* ./
COPY next.config.js ./
COPY tsconfig.json ./
COPY tailwind.config.ts ./
COPY postcss.config.js ./
COPY public ./public
COPY src ./src

# Build do Next.js
ENV NEXT_TELEMETRY_DISABLED 1
RUN npm run build

# Runner (produção)
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copiar arquivos necessários
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
