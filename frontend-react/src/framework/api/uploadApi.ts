import { submitAction } from "@/framework/api/action/submitAction"
import { submitActionMultipart } from "@/framework/api/action/submitActionMultipart"
import type {
  UploadResponse,
  UploadTempItem,
  UploadCtx,
} from "../Blocks/Action/upload/types"

/* =========================
   UPLOAD
========================= */

export async function uploadFile(
  action: string,
  file: File,
  ctx?: UploadCtx,
  onProgress?: (p: number) => void
): Promise<UploadTempItem[]> {
  const fd = new FormData()
  fd.append("files", file)

  const res =
    await submitActionMultipart<UploadResponse>(
      action,
      fd,
      {
        ctx, // ✅ теперь тип совпадает
        onProgress,
      }
    )

  return res.files
}

/* =========================
   COMMIT
========================= */

export async function commitFiles(
  action: string,
  ids: number[],
  ctx?: UploadCtx
) {
  return submitAction(
    action,
    {
      ids,
      mode: "commit",
    },
    ctx // ✅ ок
  )
}

/* =========================
   DISCARD
========================= */

export async function discardFiles(
  action: string,
  ids: number[],
  ctx?: UploadCtx
) {
  return submitAction(
    action,
    {
      ids,
      mode: "discard",
    },
    ctx // ✅ ок
  )
}