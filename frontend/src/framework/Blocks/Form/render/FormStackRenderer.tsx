import type {
  FormBlock,
  FormStackBlock,
} from "../types/types"

type Props = {
  block: FormStackBlock

  render: (
    block: FormBlock
  ) => React.ReactNode
}

export function FormStackRenderer({
  block,
  render,
}: Props) {

  return (
    <div
      className={[
        "form-stack",
        `form-stack-gap-${block.gap ?? "md"}`,
      ].join(" ")}
      style={{
        gridColumn: `span ${block.layout?.span ?? 12}`,
        order: block.layout?.order,
      }}
    >
      {block.children.map(render)}
    </div>
  )
}