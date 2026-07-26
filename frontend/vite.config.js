import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Dev server proxies the backend namespaces to the FastAPI app so the
// browser can use same-origin relative URLs (no CORS in dev).
//   - /api        → resource CRUD, cohorts, applications, ...
//   - /auth       → register / login / me
//   - /dashboard  → aggregate metrics
const BACKEND = process.env.BACKEND_URL || 'http://localhost:8000'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': { target: BACKEND, changeOrigin: true },
      '/auth': { target: BACKEND, changeOrigin: true },
      '/dashboard': { target: BACKEND, changeOrigin: true },
      '/health': { target: BACKEND, changeOrigin: true },
    },
  },
})
