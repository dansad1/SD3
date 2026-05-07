// src/framework/page/runtime/effects/handlers/toast/ToastViewport.tsx

import { createPortal } from "react-dom"
import { useToast } from "./useToast"

export function ToastViewport() {
  const { items, remove } = useToast()

  return createPortal(
    <div
      style={{
        position: "fixed",

        // не у самого края окна, а внутри main area
        top: 72,
        left: 0,
        right: 0,

        display: "flex",
        justifyContent: "center",

        zIndex: 90,
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: 1200,
          paddingLeft: 24,
          paddingRight: 24,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 8,
        }}
      >
        {items.map(item => (
          <div
            key={item.id}
            style={{
              width: "min(520px, 100%)",
              pointerEvents: "auto",
              borderRadius: 12,
              border: "1px solid",
              padding: "12px 16px",
              boxShadow: "0 12px 30px rgba(0,0,0,0.18)",
              background:
                item.variant === "success"
                  ? "#ecfdf3"
                  : item.variant === "error"
                    ? "#fef2f2"
                    : item.variant === "warning"
                      ? "#fffbeb"
                      : "#eff6ff",
              borderColor:
                item.variant === "success"
                  ? "#86efac"
                  : item.variant === "error"
                    ? "#fca5a5"
                    : item.variant === "warning"
                      ? "#fcd34d"
                      : "#93c5fd",
              color:
                item.variant === "success"
                  ? "#166534"
                  : item.variant === "error"
                    ? "#991b1b"
                    : item.variant === "warning"
                      ? "#92400e"
                      : "#1e3a8a",
            }}
          >
            <div
              style={{
                display: "flex",
                alignItems: "flex-start",
                gap: 12,
              }}
            >
              <div
                style={{
                  flex: 1,
                  minWidth: 0,
                }}
              >
                <div
                  style={{
                    fontWeight: 600,
                  }}
                >
                  {item.title}
                </div>

                {item.description && (
                  <div
                    style={{
                      marginTop: 4,
                      fontSize: 14,
                      opacity: 0.8,
                    }}
                  >
                    {item.description}
                  </div>
                )}
              </div>

              <button
                type="button"
                onClick={() => remove(item.id)}
                style={{
                  border: "none",
                  background: "transparent",
                  cursor: "pointer",
                  opacity: 0.7,
                  fontSize: 14,
                }}
              >
                ✕
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>,
    document.body
  )
}