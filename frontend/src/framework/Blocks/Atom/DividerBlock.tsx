import type { BlockComponent } from "../Registry/BlockRegistry"

export const DividerBlock: BlockComponent<"divider"> = () => {
  return (
    <div
      className="divider"
      aria-hidden="true"
    />
  )
}
