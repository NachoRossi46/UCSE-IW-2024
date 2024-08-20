/** @type {import('next').NextConfig} */
const nextConfig = {
    output: 'export',
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
  };
  
  export default nextConfig;