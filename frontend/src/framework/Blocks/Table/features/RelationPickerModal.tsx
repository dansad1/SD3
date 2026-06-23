import {
  useMemo,
  useState,
} from "react"

import {
  submitAction,
} from "@/framework/api/action/submitAction"

import {
  useTableCollection,
} from "../controller/useTableCollection"

import type {
  TableFeatureContext,
} from "./types"

import type {
  BaseRow,
} from "../types/runtime"
import Modal from "@/framework/components/ui/Modal"

type Props = {
  isOpen: boolean
  onClose: () => void
  ctx: TableFeatureContext<BaseRow>
}

function getRowLabel(row: BaseRow): string {
  const data = row as Record<string, unknown>

  const value =
    data.label ??
    data.name ??
    data.username ??
    data.title ??
    row.id

  if (
    typeof value === "string" ||
    typeof value === "number"
  ) {
    return String(value)
  }

  return String(row.id)
}

export function RelationPickerModal({
  isOpen,
  onClose,
  ctx,
}: Props) {
  const relation =
    ctx.block.relation

  const [search, setSearch] =
    useState("")

  const [selected, setSelected] =
    useState<Set<string | number>>(
      () =>
        new Set(
          ctx.list?.rows.map(
            (row) => row.id
          ) ?? []
        )
    )

  const entity =
    relation?.entity ?? ctx.entity

  const collection =
    useTableCollection<BaseRow>(
      entity || "__disabled__",
      {
        search,
      },
      {
        enabled:
          isOpen &&
          !!relation &&
          !!entity,
      }
    )

  const rows =
    collection.items

  const visibleRows =
    useMemo(() => {
      return rows
    }, [rows])

  function toggle(
    id: string | number
  ) {
    setSelected((prev) => {
      const next =
        new Set(prev)

      if (next.has(id)) {
        next.delete(id)
      } else {
        next.add(id)
      }

      return next
    })
  }

  async function save() {
    if (!relation) {
      return
    }

    await submitAction(
      "relation.set",
      {
        ids: Array.from(selected),
      },
      {
        source: relation.source,
        sourceId: relation.sourceId,
        relation: relation.relation,
      }
    )

    await ctx.list?.reload?.()

    onClose()
  }

  if (!relation) {
    return null
  }

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      width={900}
      title={
        relation.addLabel ??
        "Добавить"
      }
      footer={
        <>
          <button
            type="button"
            className="ui-btn ui-btn-secondary"
            onClick={onClose}
          >
            Отмена
          </button>

          <button
            type="button"
            className="ui-btn ui-btn-primary"
            onClick={() => {
              void save()
            }}
          >
            Сохранить
          </button>
        </>
      }
    >
      <input
        className="ui-input"
        placeholder="Поиск..."
        value={search}
        onChange={(e) =>
          setSearch(e.target.value)
        }
      />

      <div
        style={{
          maxHeight: 500,
          overflow: "auto",
          marginTop: 12,
        }}
      >
        {visibleRows.map((row) => (
          <label
            key={String(row.id)}
            style={{
              display: "flex",
              gap: 8,
              padding: 6,
              cursor: "pointer",
            }}
          >
            <input
              type="checkbox"
              checked={selected.has(row.id)}
              onChange={() =>
                toggle(row.id)
              }
            />

            <span>
              {getRowLabel(row)}
            </span>
          </label>
        ))}
      </div>
    </Modal>
  )
}