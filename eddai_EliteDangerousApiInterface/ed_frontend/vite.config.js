import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
// https://vitejs.dev/config/build-options.html#build-manifest
// https://vitejs.dev/config/build-options.html#build-emptyoutdir
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  base: process.env.NODE_ENV === "production" ? "/static-server/vuejs/" : "/",
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server:{
    port: 5173,
    host: '127.0.0.1',
    watch: {
      usePolling: true
    }
  },
  build: {
    manifest: true,
    outDir: "../static-server/vuejs/",
    emptyOutDir: true
  },
})