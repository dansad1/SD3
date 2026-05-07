import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"
import path from "path"

export default defineConfig({
  plugins: [react()],

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
    port: 5173,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
})