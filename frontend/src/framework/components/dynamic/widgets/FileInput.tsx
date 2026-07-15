import {
  useMemo,
  useRef,
  useState,
} from "react"

import {
  uploadFile,
  commitFiles,
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
const COMMIT_ACTION = "files.commit"

function getError(
  error: unknown,
): string {
  if (error instanceof Error) {
    return error.message
  }

  return "Ошибка загрузки"
}

function isFile(
  value: unknown,
): value is UploadTempItem {
  if (
    value === null ||
    typeof value !== "object"
  ) {
    return false
  }

  const candidate =
    value as Record<string, unknown>

  return (
    typeof candidate.id === "number" &&
    typeof candidate.name === "string"
  )
}

function getItems(
  value: Value,
): unknown[] {
  if (Array.isArray(value)) {
    return value
  }

  if (value == null) {
    return []
  }

  return [value]
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
    () =>
      getItems(value).filter(
        isFile,
      ),
    [value],
  )

  async function upload(
    file: File,
  ): Promise<void> {

    setUploading(true)
    setProgress(0)
    setError(undefined)

    try {

      const uploaded =
        await uploadFile(
          UPLOAD_ACTION,
          file,
          undefined,
          percent => {
            setProgress(percent)
          },
        )

      const item =
        uploaded[0]

      if (!item) {
        throw new Error(
          "Файл не загружен",
        )
      }

      await commitFiles(
        COMMIT_ACTION,
        [item.id],
      )

      if (field.multiple) {

        onChange(
          [
            ...files,
            item,
          ] as unknown as Value,
        )

      } else {

        onChange(
          item as unknown as Value,
        )

      }

    } catch (e) {

      console.error(e)

      setError(
        getError(e),
      )

    } finally {

      setUploading(false)

    }
  }

  return (
    <BaseWidget {...props}>
      {({
        disabled,
      }) => (
        <div className="file-input">

          <input
            ref={inputRef}
            hidden
            type="file"
            disabled={
              disabled ||
              uploading
            }
            onChange={event => {

              const file =
                event.target.files?.[0]

              if (file) {
                void upload(file)
              }

              event.target.value = ""

            }}
          />

          <button
            type="button"
            className="ui-input"
            disabled={
              disabled ||
              uploading
            }
            onClick={() => {
              inputRef.current?.click()
            }}
          >
            {uploading
              ? `Загрузка ${progress}%`
              : "Выбрать файл"}
          </button>

          {files.length > 0 && (
            <div className="mt-2">

              {files.map(file => (
                <div key={file.id}>

                  {file.url ? (
                    <a
                      href={file.url}
                      target="_blank"
                      rel="noreferrer"
                    >
                      {file.name}
                    </a>
                  ) : (
                    file.name
                  )}

                </div>
              ))}

            </div>
          )}

          {error && (
            <div className="text-danger mt-2">
              {error}
            </div>
          )}

        </div>
      )}
    </BaseWidget>
  )
}