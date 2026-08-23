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
        foreground: "#f3f4f6",
        navy: {
          950: "#050B18",
          900: "#0a1329",
          800: "#132145"
        },
        primary: "#00A8FF",
        ai: "#8A2BE2"
      },
    },
  },
  plugins: [],
};
export default config;
