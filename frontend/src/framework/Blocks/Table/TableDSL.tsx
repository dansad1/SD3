import type { BlockComponent } from "../Registry/BlockRegistry"
import { TableBlock } from "./render/TableBlock"
import type { TableApiBlock } from "./types/api"

export const TableDSLBlock: BlockComponent<"table"> = ({ block }) => {
  return <TableBlock block={block as TableApiBlock} />
}