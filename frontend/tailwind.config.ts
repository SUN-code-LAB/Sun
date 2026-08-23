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
        background: "#050B18",
        card: "#101B32",
        "card-border": "#1A2B4C",
        "ai-blue": "#00A8FF",
        "neon-green": "#39FF14",
        "risk-orange": "#FF8C00",
        "risk-red": "#FF0000",
        "scientific-purple": "#8A2BE2",
      },
    },
  },
  plugins: [],
};
export default config;
