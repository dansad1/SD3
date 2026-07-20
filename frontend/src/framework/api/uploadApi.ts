// src/framework/api/uploadApi.ts

import {
  submitAction,
} from "@/framework/api/action/submitAction"

import {
  submitActionMultipart,
} from "@/framework/api/action/submitActionMultipart"

import type {
  UploadActionErrorMap,
  UploadActionResult,
  UploadCtx,
} from "@/framework/Blocks/Action/upload/types"


function normalizeErrorValue(
  value: string[] | string,
): string[] {
  return Array.isArray(value)
    ? value
    : [value]
}


function getActionErrorMessage(
  errors?: UploadActionErrorMap,
): string {
  if (!errors) {
    return "Ошибка выполнения действия"
  }

  const messages = Object
    .values(errors)
    .flatMap(normalizeErrorValue)
    .filter(Boolean)

  return messages.join(", ")
    || "Ошибка выполнения действия"
}


/* =========================
   MULTIPART ACTION
========================= */

export async function uploadFile(
  action: string,
  file: File,
  ctx?: UploadCtx,
  onProgress?: (progress: number) => void,
): Promise<UploadActionResult> {
  const formData = new FormData()

  /*
   * Единое имя поля для общего upload-механизма.
   *
   * Backend action при необходимости может поддерживать
   * и "files", и "file".
   */
  formData.append(
    "files",
    file,
    file.name,
  )

  const response =
    await submitActionMultipart<
      UploadActionResult
    >(
      action,
      formData,
      {
        ctx,
        onProgress,
      },
    )

  if (
    !response
    || typeof response !== "object"
    || Array.isArray(response)
  ) {
    throw new Error(
      "Сервер вернул некорректный ответ",
    )
  }

  if (response.status === "error") {
    throw new Error(
      getActionErrorMessage(
        response.errors,
      ),
    )
  }

  return response
}


/* =========================
   COMMIT
========================= */

export async function commitFiles(
  action: string,
  ids: number[],
  ctx?: UploadCtx,
): Promise<unknown> {
  return submitAction(
    action,
    {
      ids,
      mode: "commit",
    },
    ctx,
  )
}


/* =========================
   DISCARD
========================= */

export async function discardFiles(
  action: string,
  ids: number[],
  ctx?: UploadCtx,
): Promise<unknown> {
  return submitAction(
    action,
    {
      ids,
      mode: "discard",
    },
    ctx,
  )
}