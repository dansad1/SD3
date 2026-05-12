import Button from "@/framework/components/ui/Button"
import type { UploadTempItem } from "./types"

/* =========================
   TYPES
========================= */

type RuntimeItem = {
  localId: string
  name: string
  progress: number
  status: "uploading" | "error"
}

type RuntimeListProps = {
  items: RuntimeItem[]
}

type DoneListProps = {
  items: UploadTempItem[]
  autoCommit?: boolean
  onDiscard: (id: number) => void
}

type FooterProps = {
  visible: boolean
  onCommit: () => void
}

/* =========================
   RUNTIME LIST
========================= */

export function UploadRuntimeList({ items }: RuntimeListProps) {
  if (!items.length) return null

  return (
    <div className="upload__list">
      {items.map((r: RuntimeItem) => (
        <div key={r.localId} className="upload__row">
          <div className="upload__name">{r.name}</div>

          <div className="upload__progress">
            <div
              className={`upload__progress-bar is-${r.status}`}
              style={{ width: `${r.progress}%` }}
            />
          </div>
        </div>
      ))}
    </div>
  )
}

/* =========================
   DONE LIST
========================= */

export function UploadDoneList({
  items,
  autoCommit,
  onDiscard,
}: DoneListProps) {
  if (!items.length) return null

  return (
    <div className="upload__list upload__list--done">
      {items.map((f: UploadTempItem) => (
        <div key={f.id} className="upload__row">
          <div className="upload__name">{f.name}</div>

          {!autoCommit && (
            <Button
              size="sm"
              variant="ghost"
              onClick={() => onDiscard(f.id)}
            >
              убрать
            </Button>
          )}
        </div>
      ))}
    </div>
  )
}

/* =========================
   FOOTER
========================= */

export function UploadFooter({
  visible,
  onCommit,
}: FooterProps) {
  if (!visible) return null

  return (
    <div className="upload__footer">
      <Button
        variant="primary"
        size="lg"
        onClick={onCommit}
      >
        Сохранить выбранные
      </Button>
    </div>
  )
}