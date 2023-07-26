import solid from 'vite-plugin-solid'
import { defineConfig } from 'vite'
import solidStyled from 'vite-plugin-solid-styled'
import tsconfigPaths from 'vite-tsconfig-paths'

export default defineConfig({
  plugins: [
    solid(),
    solidStyled({
      filter: {
        include: 'src/**/*.tsx',
        exclude: 'node_modules/**/*.{ts,js}',
      },
    }),
    tsconfigPaths(),
  ],
  server: {
    port: 3000,
  },
  build: {
    target: 'esnext',
  },
})
