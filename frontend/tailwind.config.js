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
        'rightPanel':'#4b4b4b',
        'text-box':'#2f2f2f',
        'message-box-ai':'#2C3A47',
        'message-box-human':'#3B3B98'
      }
    },
  },
  plugins: [],
}

