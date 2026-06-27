// ActionPresentation.tsx

import type { ActionBlock } from "../types"

import { DefaultPresentation } from "./DefaultPresentation"
import { PickerPresentation } from "./PickerPresentation"

type Props = ActionBlock

export function ActionPresentation({
  ...props
}: Props) {
  if (props.picker) {
    return (
      <PickerPresentation
        {...props}
      />
    )
  }

  return (
    <DefaultPresentation
      {...props}
    />
  )
}