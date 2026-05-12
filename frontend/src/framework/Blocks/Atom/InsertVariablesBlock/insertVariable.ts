export function formatValue(
  value: string,
  format: "template" | "raw" | "dollar"
) {
  if (format === "raw") return value
  if (format === "dollar") return `\${${value}}`
  return `{{ ${value} }}`
}
export function insertIntoField(
  fieldName: string,
  value: string
) {
  const textarea =
    document.querySelector<HTMLTextAreaElement>(
      `textarea[name="${fieldName}"]`
    )

  const input =
    document.querySelector<HTMLInputElement>(
      `input[name="${fieldName}"]`
    )

  const target = textarea || input
  if (!target) return

  const start =
    target.selectionStart ?? target.value.length
  const end =
    target.selectionEnd ?? target.value.length

  const next =
    target.value.slice(0, start) +
    value +
    target.value.slice(end)

  const proto =
    target instanceof HTMLTextAreaElement
      ? HTMLTextAreaElement.prototype
      : HTMLInputElement.prototype

  const descriptor =
    Object.getOwnPropertyDescriptor(proto, "value")

  descriptor?.set?.call(target, next)

  target.dispatchEvent(
    new Event("input", { bubbles: true })
  )

  target.focus()

  const cursor = start + value.length

  requestAnimationFrame(() => {
    target.setSelectionRange(cursor, cursor)
  })
}