// DocumentBlock.tsx

import type { DocumentBlock } from "./types"

import { DocumentView } from "./DocumentView"
import { useDocumentController } from "./useDocumentController"

export function DocumentBlock({
  block,
}: {
  block: DocumentBlock
}) {

  const vm = useDocumentController(block)

  return (
    <DocumentView
      {...vm}
    />
  )
}