// src/framework/Blocks/Action/upload/UploadWidget.tsx

import { UploadDropzone } from "./UploadDropzone"

import {
  UploadDoneList,
  UploadFooter,
  UploadRuntimeList,
} from "./UploadLists"

import { useUploadController } from "./useUploadController"

import type {
  UploadBlock,
} from "./types"


export function UploadWidget({
  block,
}: {
  block: UploadBlock
}) {
  const controller =
    useUploadController(block)

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
        multiple={block.multiple}
        accept={block.accept}
        onFiles={controller.uploadMany}
      />

      <UploadRuntimeList
        items={controller.runtime}
        onRemoveError={
          controller.removeRuntime
        }
      />

      <UploadDoneList
        items={controller.tempFiles}
        autoCommit={block.auto_commit}
        discardingIds={
          controller.discardingIds
        }
        onDiscard={controller.discardOne}
      />

      <UploadFooter
        visible={
          !block.auto_commit
          && controller.tempFiles.length > 0
        }
        disabled={
          controller.committing
          || controller.uploading
        }
        onCommit={controller.commitAll}
      />
    </div>
  )
}