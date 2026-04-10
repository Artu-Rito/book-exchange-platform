import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: true,
    open: true,
    // Проксируем ВСЕ /api запросы на backend
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        // ВАЖНО: не меняем путь, оставляем /api/v1/...
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
})
