/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx,css,scss}'],
  theme: {
    extend: {
      colors: {
        theme: {
          success: {
            light: '#e3f8e8',
            main: '#17c13e',
            dark: '#14bb38',
            200: '#8be09f',
          },
          error: {
            light: '#e48784',
            main: '#d9534f',
            dark: '#d54c48',
          },
          orange: {
            light: '#fbe9e7',
            main: '#ffab91',
            dark: '#d84315',
          },
          warning: {
            light: '#fdf5ea',
            main: '#f0ad4e',
            dark: '#ec9c3d',
          },
          grey: {
            50: '#fafafa',
            100: '#f5f5f5',
            200: '#eeeeee',
            300: '#e0e0e0',
            500: '#9e9e9e',
            600: '#757575',
            700: '#616161',
            900: '#212121',
          },
          light: {
            paper: '#FFFFFF',
            primary: {
              light: '#e4e7ec',
              main: '#203461',
              dark: '#1c2f59',
              200: '#909ab0',
              800: '#132145',
            },
            secondary: {
              light: '#fde8ef',
              main: '#ec407a',
              dark: '#ea3a72',
              200: '#f6a0bd',
              800: '#e42a5d',
            },
          },
          dark: {
            paper: '#030614',
            background: '#0a0f23',
            level: {
              1: '#070e13',
              2: '#12172f',
            },
            text: {
              title: '#e4e8f7',
              primary: '#d5d9e9',
              secondary: '#d8ddf0',
            },
            primary: {
              light: '#ecedf1',
              main: '#606d88',
              dark: '#586580',
              200: '#b0b6c4',
              800: '#44506b',
            },
            secondary: {
              light: '#fde8ef',
              main: '#ec407a',
              dark: '#ea3a72',
              200: '#f6a0bd',
              800: '#e42a5d',
            },
          },
        },
      },
    },
  },
  plugins: [],
}
