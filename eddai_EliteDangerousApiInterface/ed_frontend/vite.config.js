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
  base: '/',
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server:{
    port: 5173,
    host: '127.0.0.1',
    proxy: Object.fromEntries(
      ['/api', '/admin', '/users', '/static', '/healthz'].map((path) => [
        path,
        {
          target: process.env.DJANGO_DEV_UPSTREAM || 'http://127.0.0.1:8080',
          changeOrigin: false,
        },
      ]),
    ),
    watch: {
      usePolling: true
    }
  },
  build: {
    manifest: true,
    outDir: 'dist',
    emptyOutDir: true
  },
})