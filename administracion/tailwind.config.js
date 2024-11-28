/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/web/templates/**/*.html',
    './src/**/*.py',
    "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    extend: {},
  },
  plugins: [require('flowbite/plugin')({
    datatables:true,
  })
  ],
}
