import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  typescript: {
    ignoreBuildErrors: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
  api: {
    bodyParser: {
      sizeLimit: '10mb' // Set your preferred limit (up to 50mb)
    }
  },
  
  images: {
    domains: ['localhost'],
  },
};

export default nextConfig;
