import { AuthProvider } from "@/framework/auth/AuthProvider"
import AppRoutes from "@/Project/routes"
import { SurfaceRoot } from "@/framework/Surface/SurfaceRoot"

import { FrameworkErrorBoundary } from "@/framework/trace/FrameworkErrorBoundary"
import { TraceDevtools } from "@/framework/trace/Devtools"

import { ToastProvider } from "@/framework/page/runtime/effects/handlers/toast/ToastProvider"
import { ToastViewport } from "@/framework/page/runtime/effects/handlers/toast/ToastViewport"

export default function App() {
  return (
    <FrameworkErrorBoundary>
      <TraceDevtools />

      <AuthProvider>
        <ToastProvider>
          <SurfaceRoot>
            <AppRoutes />
          </SurfaceRoot>

          <ToastViewport />
        </ToastProvider>
      </AuthProvider>
    </FrameworkErrorBoundary>
  )
}