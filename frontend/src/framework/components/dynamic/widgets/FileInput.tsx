// src/framework/components/dynamic/widgets/FileInput.tsx

import {
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
  WidgetRenderer,
} from "../types"

const UPLOAD_ACTION = "files.upload"

const COMMIT_ACTION = "files.commit"

function getError(
  error: unknown,
): string {

  if (
    error instanceof Error
  ) {
    return error.message
  }

  return "Ошибка загрузки"

}

export const FileInputWidget: WidgetRenderer = (
  props,
) => {

  const {
    value,
    onChange,
  } = props

  const inputRef =
    useRef<HTMLInputElement>(
      null,
    )

  const [
    uploading,
    setUploading,
  ] = useState(false)

  const [
    progress,
    setProgress,
  ] = useState(0)

  const [
    fileName,
    setFileName,
  ] = useState<string>()

  const [
    error,
    setError,
  ] = useState<string>()

  async function upload(
    file: File,
  ) {

    setUploading(true)

    setProgress(0)

    setError(undefined)

    try {

      const uploaded =
        await uploadFile(

          UPLOAD_ACTION,

          file,

          undefined,

          p =>
            setProgress(p),

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

        [
          item.id,
        ],

      )

      setFileName(
        item.name,
      )

      onChange(
        item.id,
      )

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
              disabled
              || uploading
            }

            onChange={e => {

              const file =
                e.target.files?.[0]

              if (
                file
              ) {

                void upload(
                  file,
                )

              }

              e.target.value = ""

            }}

          />

          <button

            type="button"

            className="ui-input"

            disabled={
              disabled
              || uploading
            }

            onClick={() =>
              inputRef.current?.click()
            }

          >

            {uploading

              ? `Загрузка ${progress}%`

              : "Выбрать файл"}

          </button>

          {fileName && (

            <div className="mt-2">

              {fileName}

            </div>

          )}

          {!fileName && value && (

            <div className="mt-2">

              Файл #

              {String(
                value,
              )}

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