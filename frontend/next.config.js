/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  trailingSlash: false,
  images: {
    domains: ['localhost', '192.168.1.2'],
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api',
  },
  async rewrites() {
    return [
      {
        source: '/api/search/status',
        destination: 'http://localhost:8000/api/search/status/',
      },
      {
        source: '/api/search/suggest',
        destination: 'http://localhost:8000/api/search/suggest/',
      },
      {
        source: '/api/search/boolean',
        destination: 'http://localhost:8000/api/search/boolean/',
      },
      {
        source: '/api/search/files',
        destination: 'http://localhost:8000/api/search/files/',
      },
      {
        source: '/api/search',
        destination: 'http://localhost:8000/api/search/',
      },
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ]
  },
}

module.exports = nextConfig