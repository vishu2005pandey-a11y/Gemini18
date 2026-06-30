import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Premium blue-purple theme
        bg: {
          primary:   "#0a0a0f",   // deepest background
          secondary: "#111118",   // card background
          tertiary:  "#1a1a24",   // elevated card
          border:    "#2a2a3a",   // borders
        },
        accent: {
          primary:   "#6c63ff",   // main purple
          secondary: "#4f8eff",   // blue accent
          glow:      "#6c63ff33", // glow shadow
          gradient:  "linear-gradient(135deg, #6c63ff 0%, #4f8eff 100%)",
        },
        text: {
          primary:   "#ffffff",
          secondary: "#8888aa",
          muted:     "#555566",
        },
        success: "#22d3a5",
        danger:  "#ff4f6e",
        warning: "#f5a623",
      },
      backgroundImage: {
        "accent-gradient": "linear-gradient(135deg, #6c63ff 0%, #4f8eff 100%)",
        "card-gradient":   "linear-gradient(135deg, #1a1a24 0%, #111118 100%)",
        "wallet-gradient": "linear-gradient(135deg, #6c63ff 0%, #4f8eff 60%, #22d3a5 100%)",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      boxShadow: {
        accent: "0 0 20px #6c63ff44",
        card:   "0 4px 24px #00000066",
      },
      borderRadius: {
        "2xl": "1rem",
        "3xl": "1.5rem",
      },
    },
  },
  plugins: [],
};

export default config;
