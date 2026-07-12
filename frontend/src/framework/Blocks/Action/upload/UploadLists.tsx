// src/framework/Blocks/Action/upload/UploadLists.tsx

import Button from "@/framework/components/ui/Button"

import type {
  UploadRuntimeItem,
  UploadTempItem,
} from "./types"


type RuntimeListProps = {
  items: UploadRuntimeItem[]

  onRemoveError?: (
    localId: string,
  ) => void
}


type DoneListProps = {
  items: UploadTempItem[]

  autoCommit?: boolean

  discardingIds?: Set<number>

  onDiscard: (
    id: number,
  ) => void
}


type FooterProps = {
  visible: boolean
  disabled?: boolean

  onCommit: () => void
}


function formatSize(
  size?: number,
): string | null {
  if (
    size == null
    || size < 0
  ) {
    return null
  }

  if (size < 1024) {
    return `${size} Б`
  }

  if (size < 1024 * 1024) {
    return `${
      Math.round(size / 1024)
    } КБ`
  }

  return `${
    (
      size
      / 1024
      / 1024
    ).toFixed(1)
  } МБ`
}


export function UploadRuntimeList({
  items,
  onRemoveError,
}: RuntimeListProps) {
  if (!items.length) {
    return null
  }

  return (
    <div className="upload__list">
      {items.map(item => (
        <div
          key={item.localId}
          className="upload__row"
        >
          <div className="upload__content">
            <div className="upload__name">
              {item.name}
            </div>

            <div className="upload__progress">
              <div
                className={[
                  "upload__progress-bar",
                  `is-${item.status}`,
                ].join(" ")}
                style={{
                  width:
                    `${item.progress}%`,
                }}
              />
            </div>

            {item.status === "error" && (
              <div className="upload__error">
                {item.error
                  ?? "Ошибка загрузки"}
              </div>
            )}
          </div>

          {item.status === "error" && (
            <Button
              size="sm"
              variant="ghost"
              onClick={() =>
                onRemoveError?.(
                  item.localId,
                )
              }
            >
              убрать
            </Button>
          )}
        </div>
      ))}
    </div>
  )
}


export function UploadDoneList({
  items,
  autoCommit,
  discardingIds,
  onDiscard,
}: DoneListProps) {
  if (!items.length) {
    return null
  }

  return (
    <div className="upload__list upload__list--done">
      {items.map(item => {
        const removing =
          discardingIds?.has(
            item.id,
          ) ?? false

        const size =
          formatSize(item.size)

        return (
          <div
            key={item.id}
            className="upload__row"
          >
            <div className="upload__content">
              {item.url ? (
                <a
                  className="upload__name"
                  href={item.url}
                  target="_blank"
                  rel="noreferrer"
                >
                  {item.name}
                </a>
              ) : (
                <div className="upload__name">
                  {item.name}
                </div>
              )}

              {size && (
                <div className="upload__size">
                  {size}
                </div>
              )}
            </div>

            {!autoCommit && (
              <Button
                size="sm"
                variant="ghost"
                disabled={removing}
                onClick={() =>
                  onDiscard(item.id)
                }
              >
                {removing
                  ? "..."
                  : "убрать"}
              </Button>
            )}
          </div>
        )
      })}
    </div>
  )
}


export function UploadFooter({
  visible,
  disabled,
  onCommit,
}: FooterProps) {
  if (!visible) {
    return null
  }

  return (
    <div className="upload__footer">
      <Button
        variant="primary"
        size="lg"
        disabled={disabled}
        onClick={onCommit}
      >
        {disabled
          ? "Сохранение..."
          : "Сохранить выбранные"}
      </Button>
    </div>
  )
}