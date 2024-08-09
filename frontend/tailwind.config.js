/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      backgroundColor:{
        'leftPanel':'#3d3d3d',
        'rightPanel':'#4b4b4b'
      }
    },
  },
  plugins: [],
}

