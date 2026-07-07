import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// The `base` path is set via env var so the same build works for
// user.github.io/repo-name (needs "/repo-name/") and custom domains ("/").
export default defineConfig({
  base: process.env.VITE_BASE_PATH || "/",
  plugins: [react()],
  build: {
    outDir: "dist",
    sourcemap: false
  }
});
