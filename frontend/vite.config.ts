import path from "path"

import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"


export default defineConfig({
  plugins: [
    react(),
  ],

  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },

    dedupe: [
      "ckeditor5",
      "@ckeditor/ckeditor5-react",
      "@ckeditor/ckeditor5-core",
      "@ckeditor/ckeditor5-engine",
      "@ckeditor/ckeditor5-utils",
      "@ckeditor/ckeditor5-ui",
    ],
  },

  optimizeDeps: {
    include: [
      "ckeditor5",
      "@ckeditor/ckeditor5-react",
    ],
  },

  server: {
    host: "0.0.0.0",
    port: 5173,

    watch: {
      usePolling: true,
    },

    proxy: {
      "/api": {
        target: "http://backend:8000",
        changeOrigin: true,
      },
      "/media": {
        target: "http://backend:8000",
        changeOrigin: true,
      },
      "/static": {
        target: "http://backend:8000",
        changeOrigin: true,
      },
    },
  },
})