import { useUploadController } from "./useUploadController"
import { UploadDropzone } from "./UploadDropzone"
import {
  UploadRuntimeList,
  UploadDoneList,
  UploadFooter,
} from "./UploadLists"
import type { UploadBlock } from "./types"

export function UploadWidget({ block }: { block: UploadBlock }) {
  const ctrl = useUploadController(block)

  return (
    <div className="upload">
      {block.label && (
        <div className="upload__label">
          {block.label}
        </div>
      )}

      <UploadDropzone
        disabled={ctrl.disabled}
        multiple={block.multiple}
        accept={block.accept}
        onFiles={ctrl.uploadMany}
      />

      <UploadRuntimeList items={ctrl.runtime} />

      <UploadDoneList
        items={ctrl.tempFiles}
        autoCommit={block.auto_commit}
        onDiscard={ctrl.discardOne}
      />

      <UploadFooter
        visible={
          !block.auto_commit && ctrl.tempFiles.length > 0
        }
        onCommit={ctrl.commitAll}
      />
    </div>
  )
}