import type { BlockComponent } from "../Registry/BlockRegistry"

const TAGS = {
  1: "h1",
  2: "h2",
  3: "h3",
  4: "h4",
} as const

export const HeadingBlock: BlockComponent<"heading"> = ({ block }) => {

  const level = block.level ?? 2
  const Tag = TAGS[level] ?? "h2"

  const text = block.text || block.fallback || ""

  return <Tag>{text}</Tag>
}
