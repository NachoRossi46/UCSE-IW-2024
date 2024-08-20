/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    swcMinify: true,
    images: {
      domains: ['tu-dominio-de-imagenes.com'],
    },
    env: {
      customKey: process.env.CUSTOM_KEY,
      // Añade aquí otras variables de entorno que necesites
      NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
    },
    // Añade aquí otras configuraciones específicas de tu proyecto
    async rewrites() {
      return [
        {
          source: '/api/:path*',
          destination: `${process.env.NEXT_PUBLIC_API_URL}/api/:path*`,
        },
      ];
    },
  };
  
  export default nextConfig;