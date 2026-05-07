// src/devtools/TraceDevtools.tsx

import { useEffect, useState } from "react"
import { TracePanel } from "./TracePanel"

export function TraceDevtools() {
  const [open, setOpen] = useState(false)

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === "t") {
        setOpen(v => !v)
      }
    }

    window.addEventListener("keydown", handler)
    return () => window.removeEventListener("keydown", handler)
  }, [])

  return (
    <>
      <button
        onClick={() => setOpen(v => !v)}
        style={{
          position: "fixed",
          right: 16,
          bottom: 16,
          zIndex: 100000,
          padding: "10px 14px",
          borderRadius: 12,
          border: "1px solid #e5e7eb",
          background: "#111827",
          color: "#fff",
          cursor: "pointer",
          fontSize: 12,
        }}
      >
        TRACE
      </button>

      <TracePanel
        open={open}
        onClose={() => setOpen(false)}
      />
    </>
  )
}