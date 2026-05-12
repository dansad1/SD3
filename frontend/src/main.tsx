// src/main.tsx

import "@/Project/styles/index.ts"

import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import { BrowserRouter } from "react-router-dom"

import App from "./App"

import { traceSessionStore } from "@/framework/trace/TraceSessionStore"
import { initUIActions } from "./framework/Blocks/Action/actions/initUIActions"
import { initFormLayout } from "./framework/Blocks/Form/Layout/init"

/* =========================================================
   UI ACTIONS INIT
========================================================= */

initUIActions()
initFormLayout() // 👈 ВОТ ЭТО КРИТИЧНО
/* =========================================================
   ⭐ GLOBAL BOOT TRACE
========================================================= */

window.addEventListener("error", (e) => {
  traceSessionStore.push({
    id: crypto.randomUUID(),
    page: location.pathname,
    trigger: "mount",
    status: "error",
    startedAt: Date.now(),
    finishedAt: Date.now(),
    summary: e.message,
    root: {
      id: crypto.randomUUID(),
      name: "bootstrap_error",
      status: "error",
      startedAt: Date.now(),
      finishedAt: Date.now(),
      meta: {
        error: e.message,
        filename: e.filename,
        lineno: e.lineno,
        colno: e.colno,
      },
      children: [],
    },
  })
})

window.addEventListener("unhandledrejection", (e) => {
  traceSessionStore.push({
    id: crypto.randomUUID(),
    page: location.pathname,
    trigger: "mount",
    status: "error",
    startedAt: Date.now(),
    finishedAt: Date.now(),
    summary: String(e.reason),
    root: {
      id: crypto.randomUUID(),
      name: "bootstrap_promise_error",
      status: "error",
      startedAt: Date.now(),
      finishedAt: Date.now(),
      meta: {
        error: String(e.reason),
      },
      children: [],
    },
  })
})

/* ========================================================= */

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>
)