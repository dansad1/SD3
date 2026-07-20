import {
  ActionResultView,
} from "./ActionResultView"
import type { UploadBlock } from "./types"
import { UploadDropzone } from "./UploadDropzone"
import { UploadDoneList, UploadFooter, UploadRuntimeList } from "./UploadLists"
import { useUploadController } from "./useUploadController"


export function UploadWidget({
  block,
}: {
  block: UploadBlock
}) {
  const controller =
    useUploadController(
      block,
    )

  const supportsStoredFiles =
    Boolean(
      block.result_key,
    )

  const supportsCommit =
    supportsStoredFiles
    && Boolean(
      block.commit_action,
    )

  return (
    <div className="upload">
      {block.label && (
        <div className="upload__label">
          {block.label}
        </div>
      )}

      <UploadDropzone
        disabled={
          controller.disabled
          || controller.uploading
        }
        multiple={
          block.multiple
        }
        accept={
          block.accept
        }
        onFiles={
          controller.uploadMany
        }
      />

      <UploadRuntimeList
        items={
          controller.runtime
        }
        onRemoveError={
          controller.removeRuntime
        }
      />

      {supportsStoredFiles && (
        <UploadDoneList
          items={
            controller.tempFiles
          }
          autoCommit={
            block.auto_commit
          }
          discardingIds={
            controller.discardingIds
          }
          onDiscard={
            controller.discardOne
          }
        />
      )}

      <ActionResultView
        result={
          controller.result
        }
      />

      <UploadFooter
        visible={
          supportsCommit
          && !block.auto_commit
          && controller.tempFiles.length > 0
        }
        disabled={
          controller.committing
          || controller.uploading
        }
        onCommit={
          controller.commitAll
        }
      />
    </div>
  )
}