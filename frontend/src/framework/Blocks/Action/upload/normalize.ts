import { normalizeId } from "@/framework/normalize/normalizeCommon";
import type { UploadBlock } from "./types";

export function normalizeUpload(
  block: UploadBlock
): UploadBlock {

  return {
    ...block,
    id: normalizeId(block.id),
    files: block.files ?? [],
    multiple: block.multiple ?? true,
  }
}