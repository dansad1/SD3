import type { ReactNode } from "react"
import type { Option } from "./types"

type Props = {
  options: Option[]
  value: unknown
  multiple?: boolean
  onChange: (v: unknown) => void
  children: (
    option: Option,
    ctx: {
      checked: boolean
      toggle: () => void
    }
  ) => ReactNode
}

/* ================= utils ================= */

function normalize(v: unknown): string {
  return String(v)
}

function isSelected(
  selected: unknown,
  value: string | number,
  multiple?: boolean
) {

  if (multiple) {

    if (!Array.isArray(selected)) return false

    const list = selected.map(normalize)

    return list.includes(normalize(value))
  }

  return normalize(selected) === normalize(value)
}

function toggleValue(
  selected: unknown,
  value: string | number,
  multiple?: boolean
) {

  if (multiple) {

    const list = Array.isArray(selected)
      ? selected.map(normalize)
      : []

    const v = normalize(value)

    if (list.includes(v)) {
      return list.filter(x => x !== v)
    }

    return [...list, v]
  }

  return normalize(value)
}

/* ================= component ================= */

export function OptionIterator({
  options,
  value,
  multiple,
  onChange,
  children,
}: Props) {

  function toggle(v: string | number) {

    const next = toggleValue(value, v, multiple)

    onChange(next)
  }

  return (
    <>
      {options.map(option => {

        const checked = isSelected(
          value,
          option.value,
          multiple
        )

        return children(option, {
          checked,
          toggle: () => toggle(option.value),
        })

      })}
    </>
  )
}