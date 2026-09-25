/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        leaf: { 50: "#f1f9f0", 100: "#dcf0da", 500: "#4c9a2a", 600: "#3d7d21", 700: "#2f5f19" },
        earth: { 50: "#fbf7f0", 500: "#a9762f", 700: "#7a5420" },
      },
    },
  },
  plugins: [],
}
