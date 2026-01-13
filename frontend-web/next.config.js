/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  // Desabilitar otimização de imagens do Next.js (não funciona bem em containers)
  images: {
    unoptimized: true,
    domains: ['localhost', 'hdt-energy-facial.mqtl34.easypanel.host'],
  },
}

module.exports = nextConfig
