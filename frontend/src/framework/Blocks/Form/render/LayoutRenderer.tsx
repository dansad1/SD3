import {
  isSectionBlock,
  isStackBlock,
  isTabsBlock,
  type FormBlock,
} from "../types/types"

import {
  FormSectionRenderer,
} from "./FormSectionRenderer"

import {
  FormStackRenderer,
} from "./FormStackRenderer"

import {
  FormTabsRenderer,
} from "./FormTabsRenderer"

type Props = {
  block: FormBlock

  render: (
    block: FormBlock
  ) => React.ReactNode
}

export function LayoutRenderer({
  block,
  render,
}: Props) {

  if (isSectionBlock(block)) {
    return (
      <FormSectionRenderer
        block={block}
        render={render}
      />
    )
  }

  if (isStackBlock(block)) {
    return (
      <FormStackRenderer
        block={block}
        render={render}
      />
    )
  }

  if (isTabsBlock(block)) {
  return (
    <FormTabsRenderer
      block={block}
      render={render}
    />
  )
}

  return null
}