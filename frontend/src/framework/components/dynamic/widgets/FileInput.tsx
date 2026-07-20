import {
  useMemo,
  useRef,
  useState,
} from "react"

import {
  uploadFile,
} from "@/framework/api/uploadApi"

import {
  BaseWidget,
} from "./Base"

import type {
  Value,
  WidgetRenderer,
} from "../types"

import type {
  UploadTempItem,
} from "@/framework/Blocks/Action/upload/types"


const UPLOAD_ACTION = "files.upload"


type FileRecord = {
  id?: unknown
  pk?: unknown
  value?: unknown

  name?: unknown
  filename?: unknown
  original_name?: unknown

  size?: unknown
  mime_type?: unknown

  url?: unknown
  download_url?: unknown
}


type FileFieldOptions = {
  accept?: unknown
  max_size?: unknown
  max_files?: unknown
}


function getErrorMessage(
  error: unknown,
): string {
  if (
    error instanceof Error
    && error.message
  ) {
    return error.message
  }

  return "Ошибка загрузки файла"
}


function normalizeId(
  value: unknown,
): number | null {
  if (
    typeof value === "number"
    && Number.isFinite(value)
    && value > 0
  ) {
    return value
  }

  if (
    typeof value === "string"
    && value.trim() !== ""
  ) {
    const parsed = Number(
      value,
    )

    if (
      Number.isFinite(parsed)
      && parsed > 0
    ) {
      return parsed
    }
  }

  return null
}


function normalizeString(
  value: unknown,
): string | undefined {
  if (
    typeof value === "string"
    && value.trim() !== ""
  ) {
    return value
  }

  return undefined
}


function normalizeNumber(
  value: unknown,
): number | undefined {
  if (
    typeof value === "number"
    && Number.isFinite(value)
  ) {
    return value
  }

  if (
    typeof value === "string"
    && value.trim() !== ""
  ) {
    const parsed = Number(
      value,
    )

    if (Number.isFinite(parsed)) {
      return parsed
    }
  }

  return undefined
}


function toFileItem(
  value: unknown,
): UploadTempItem | null {
  if (
    typeof value === "number"
    || typeof value === "string"
  ) {
    const id = normalizeId(
      value,
    )

    if (id === null) {
      return null
    }

    return {
      id,
      name: `Файл #${id}`,
    }
  }

  if (
    value === null
    || typeof value !== "object"
  ) {
    return null
  }

  const candidate =
    value as FileRecord

  const id = normalizeId(
    candidate.id
    ?? candidate.pk
    ?? candidate.value,
  )

  if (id === null) {
    return null
  }

  const name =
    normalizeString(
      candidate.name,
    )
    ?? normalizeString(
      candidate.original_name,
    )
    ?? normalizeString(
      candidate.filename,
    )
    ?? `Файл #${id}`

  const url =
    normalizeString(
      candidate.url,
    )
    ?? normalizeString(
      candidate.download_url,
    )

  return {
    id,
    name,
    size: normalizeNumber(
      candidate.size,
    ),
    mime_type: normalizeString(
      candidate.mime_type,
    ),
    url,
  }
}


function getItems(
  value: Value,
): UploadTempItem[] {
  const source: unknown[] =
    Array.isArray(value)
      ? value as unknown[]
      : value == null
        ? []
        : [value]

  return source
    .map(toFileItem)
    .filter(
      (
        item,
      ): item is UploadTempItem =>
        item !== null,
    )
}


function mergeFiles(
  current: UploadTempItem[],
  uploaded: UploadTempItem[],
): UploadTempItem[] {
  const result = [
    ...current,
  ]

  const existingIds = new Set(
    current.map(
      file => file.id,
    ),
  )

  for (const file of uploaded) {
    if (existingIds.has(file.id)) {
      continue
    }

    existingIds.add(
      file.id,
    )

    result.push(
      file,
    )
  }

  return result
}


function formatFileSize(
  size: number | undefined,
): string {
  if (
    size === undefined
    || !Number.isFinite(size)
    || size < 0
  ) {
    return "—"
  }

  if (size < 1024) {
    return `${size} Б`
  }

  if (size < 1024 * 1024) {
    return `${
      Math.round(
        size / 1024,
      )
    } КБ`
  }

  return `${
    (
      size
      / 1024
      / 1024
    ).toFixed(1)
  } МБ`
}


export const FileInputWidget: WidgetRenderer = (
  props,
) => {
  const {
    value,
    onChange,
    field,
  } = props

  const inputRef =
    useRef<HTMLInputElement>(null)

  const [
    uploading,
    setUploading,
  ] = useState(false)

  const [
    progress,
    setProgress,
  ] = useState(0)

  const [
    error,
    setError,
  ] = useState<string>()

  const files = useMemo(
    () => getItems(value),
    [value],
  )

  const options =
    (
      field.options
      ?? {}
    ) as FileFieldOptions

  const accept =
    typeof options.accept === "string"
      ? options.accept
      : undefined

  const maxSize =
    normalizeNumber(
      options.max_size,
    )

  const maxFiles =
    normalizeNumber(
      options.max_files,
    )

  function updateValue(
    nextFiles: UploadTempItem[],
  ): void {
    if (field.multiple) {
      onChange(
        nextFiles as unknown as Value,
      )

      return
    }

    onChange(
      (
        nextFiles[0]
        ?? null
      ) as unknown as Value,
    )
  }

  function validateSelectedFiles(
    selectedFiles: File[],
  ): File[] {
    let result = [
      ...selectedFiles,
    ]

    if (!field.multiple) {
      result = result.slice(
        0,
        1,
      )
    }

    if (
      field.multiple
      && maxFiles !== undefined
    ) {
      const available =
        Math.max(
          0,
          maxFiles - files.length,
        )

      if (available === 0) {
        throw new Error(
          `Можно загрузить не более ${maxFiles} файлов`,
        )
      }

      result = result.slice(
        0,
        available,
      )
    }

    if (maxSize !== undefined) {
      const tooLargeFile =
        result.find(
          file => file.size > maxSize,
        )

      if (tooLargeFile) {
        throw new Error(
          `Файл "${tooLargeFile.name}" превышает допустимый размер`,
        )
      }
    }

    return result
  }

  async function uploadOne(
    file: File,
  ): Promise<UploadTempItem[]> {
    const uploaded =
      await uploadFile(
        UPLOAD_ACTION,
        file,
        undefined,
        percent => {
          setProgress(
            percent,
          )
        },
      )

    if (
      !Array.isArray(uploaded)
      || uploaded.length === 0
    ) {
      throw new Error(
        "Сервер не вернул загруженный файл",
      )
    }

    return uploaded
      .map(toFileItem)
      .filter(
        (
          item,
        ): item is UploadTempItem =>
          item !== null,
      )
  }

  async function uploadSelected(
    selectedFiles: File[],
  ): Promise<void> {
    if (
      uploading
      || selectedFiles.length === 0
    ) {
      return
    }

    setUploading(true)
    setProgress(0)
    setError(undefined)

    try {
      const filesToUpload =
        validateSelectedFiles(
          selectedFiles,
        )

      const uploadedFiles:
        UploadTempItem[] = []

      for (const file of filesToUpload) {
        const uploaded =
          await uploadOne(
            file,
          )

        uploadedFiles.push(
          ...uploaded,
        )
      }

      if (
        uploadedFiles.length === 0
      ) {
        throw new Error(
          "Не удалось получить данные загруженного файла",
        )
      }

      if (field.multiple) {
        updateValue(
          mergeFiles(
            files,
            uploadedFiles,
          ),
        )

        return
      }

      updateValue(
        uploadedFiles.slice(
          0,
          1,
        ),
      )
    } catch (uploadError) {
      console.error(
        "File upload failed",
        uploadError,
      )

      setError(
        getErrorMessage(
          uploadError,
        ),
      )
    } finally {
      setUploading(false)
      setProgress(0)
    }
  }

  function removeFile(
    id: number,
  ): void {
    updateValue(
      files.filter(
        file => file.id !== id,
      ),
    )
  }

  return (
    <BaseWidget {...props}>
      {({
        disabled,
      }) => (
        <>
          <input
            ref={inputRef}
            hidden
            type="file"
            accept={accept}
            multiple={
              Boolean(
                field.multiple,
              )
            }
            disabled={
              disabled
              || uploading
            }
            onChange={event => {
              const selectedFiles =
                Array.from(
                  event.target.files
                  ?? [],
                )

              event.target.value = ""

              if (
                selectedFiles.length > 0
              ) {
                void uploadSelected(
                  selectedFiles,
                )
              }
            }}
          />

          <div className="ui-list-toolbar">
            <div className="ui-list-toolbar__left">
              <button
                type="button"
                className={[
                  "ui-btn",
                  "ui-btn-secondary",
                  "ui-btn-sm",
                  uploading
                    ? "is-loading"
                    : "",
                ]
                  .filter(Boolean)
                  .join(" ")}
                disabled={
                  disabled
                  || uploading
                }
                onClick={() => {
                  inputRef.current?.click()
                }}
              >
                <span className="ui-btn-label">
                  {uploading
                    ? `Загрузка ${progress}%`
                    : "Выбрать файл"}
                </span>
              </button>
            </div>

            <div className="ui-list-toolbar__right">
              {files.length > 0 && (
                <span>
                  Файлов: {files.length}
                </span>
              )}
            </div>
          </div>

          {files.length > 0 && (
            <div className="ui-table-wrapper">
              <table className="ui-table">
                <thead>
                  <tr>
                    <th>
                      Файл
                    </th>

                    <th>
                      Тип
                    </th>

                    <th>
                      Размер
                    </th>

                    {!disabled && (
                      <th>
                        Действия
                      </th>
                    )}
                  </tr>
                </thead>

                <tbody>
                  {files.map(file => (
                    <tr key={file.id}>
                      <td>
                        {file.url ? (
                          <a
                            href={file.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className={[
                              "ui-link",
                              "variant-default",
                              "underline-hover",
                              "size-md",
                              "external",
                            ].join(" ")}
                          >
                            <span className="ui-link-label">
                              {file.name}
                            </span>

                            <span
                              className="ui-link-external"
                              aria-hidden="true"
                            >
                              ↗
                            </span>
                          </a>
                        ) : (
                          <span>
                            {file.name}
                          </span>
                        )}
                      </td>

                      <td>
                        {file.mime_type ?? "—"}
                      </td>

                      <td>
                        {formatFileSize(
                          file.size,
                        )}
                      </td>

                      {!disabled && (
                        <td>
                          <button
                            type="button"
                            className={[
                              "ui-btn",
                              "ui-btn-danger",
                              "ui-btn-sm",
                            ].join(" ")}
                            disabled={uploading}
                            onClick={() => {
                              removeFile(
                                file.id,
                              )
                            }}
                          >
                            <span className="ui-btn-label">
                              Удалить
                            </span>
                          </button>
                        </td>
                      )}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {error && (
            <div
              className="table-selection-panel"
              role="alert"
            >
              <span className="text-danger">
                {error}
              </span>
            </div>
          )}
        </>
      )}
    </BaseWidget>
  )
}