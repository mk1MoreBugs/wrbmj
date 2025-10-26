import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vueDevTools from 'vite-plugin-vue-devtools'
import tailwindcss from '@tailwindcss/vite'

//const isProduction = process.env.ENVIRONMENT === 'production'
// https://vite.dev/config/
export default defineConfig(({ command, mode, isSsrBuild, isPreview }) => {
  const commonConfig = {
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      }
    }
  }

  if (command === 'serve') {
    return {
      // dev specific config
      ...commonConfig,
      plugins: [
        vue(),
        vueJsx(),
        vueDevTools(),
        tailwindcss(),
      ],
      server: {
        port: 8080,
      },
    }
  } else {
    // command === 'build'

    return {
      // build specific config
      ...commonConfig,
      plugins: [
        vue(),
        vueJsx(),
        tailwindcss(),
      ],
      build: {
        target: 'esnext',
        sourcemap: false
      },
    }
  }
})