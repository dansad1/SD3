import { useActionExecutor } from "./executor/useActionExecutor"
import type { ActionContext } from "./types"

type Props = {
  label: string

  to?: string
  action?: string

  ctx?: ActionContext
  variant?: "primary" | "secondary" | "ghost" | "danger"
}

export function ActionBlock({
  label,
  to,
  action,
  ctx,
  variant = "secondary",
}: Props) {
  const { runAction, isRunning } = useActionExecutor()

  // 🔥 теперь строго
  const finalAction = action ?? to

  if (!finalAction) {
    console.warn("ActionBlock: no 'to' or 'action' provided")
    return null
  }

  const loading = isRunning(finalAction)

  return (
    <button
      type="button"
      className={`ui-btn ui-btn-${variant}`}
      disabled={loading}
      onClick={() => void runAction(finalAction, ctx)}
    >
      {loading ? "..." : label}
    </button>
  )
}