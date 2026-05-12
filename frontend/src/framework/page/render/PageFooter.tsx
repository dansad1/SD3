import type { ActionDescriptor } from "../../Blocks/Action/types"

interface Props {
  actions: ActionDescriptor[]
  run: (id: string) => Promise<unknown>
  isRunning?: (id: string) => boolean
}

export function PageFooter({
  actions,
  run,
  isRunning,
}: Props) {
  console.log("📦 PAGE FOOTER RENDER", { actions })

  // 🔥 фильтрация ТОЛЬКО тут
  const visibleActions = actions.filter(
  a => a.label && a.id !== "form:setValue"
)

  if (!visibleActions.length) return null

  const handleClick = async (id: string) => {
    try {
      await run(id)
    } catch (e) {
      console.error(e)
    }
  }

  return (
    <div className="page-footer">
      {visibleActions.map(action => {
        const loading = isRunning?.(action.id)

        const cls =
          action.variant === "danger"
            ? "ui-btn ui-btn-danger"
            : action.variant === "secondary"
            ? "ui-btn ui-btn-secondary"
            : action.variant === "ghost"
            ? "ui-btn ui-btn-ghost"
            : "ui-btn ui-btn-primary"

        return (
          <button
            key={action.id}
            className={cls}
            disabled={loading}
            onClick={() => void handleClick(action.id)}
          >
            {loading ? "..." : action.label}
          </button>
        )
      })}
    </div>
  )
}