/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_BOT_API: process.env.NEXT_PUBLIC_BOT_API || "",
    NEXT_PUBLIC_BOT_USERNAME: process.env.NEXT_PUBLIC_BOT_USERNAME || "GammaChkerbot",
  },
};

module.exports = nextConfig;
