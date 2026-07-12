// src/framework/Blocks/Action/upload/UploadDropzone.tsx

import {
  useRef,
  useState,
} from "react"


type UploadDropzoneProps = {
  onFiles: (
    files: File[],
  ) => void

  disabled?: boolean
  multiple?: boolean
  accept?: string
}


export function UploadDropzone({
  onFiles,
  disabled = false,
  multiple = false,
  accept,
}: UploadDropzoneProps) {
  const inputRef =
    useRef<HTMLInputElement>(null)

  const [
    dragging,
    setDragging,
  ] = useState(false)

  function open(): void {
    if (disabled) {
      return
    }

    inputRef.current?.click()
  }

  function submitFiles(
    fileList: FileList | null,
  ): void {
    if (
      disabled
      || !fileList
    ) {
      return
    }

    const files =
      Array.from(fileList)

    onFiles(
      multiple
        ? files
        : files.slice(0, 1),
    )
  }

  return (
    <>
      <input
        ref={inputRef}
        type="file"
        hidden
        multiple={multiple}
        accept={accept}
        disabled={disabled}
        onChange={event => {
          submitFiles(
            event.target.files,
          )

          event.target.value = ""
        }}
      />

      <div
        role="button"
        tabIndex={disabled ? -1 : 0}
        className={[
          "upload__dropzone",
          disabled
            ? "is-disabled"
            : "",
          dragging
            ? "is-dragging"
            : "",
        ]
          .filter(Boolean)
          .join(" ")}
        onClick={open}
        onKeyDown={event => {
          if (
            event.key === "Enter"
            || event.key === " "
          ) {
            event.preventDefault()
            open()
          }
        }}
        onDragEnter={event => {
          event.preventDefault()

          if (!disabled) {
            setDragging(true)
          }
        }}
        onDragOver={event => {
          event.preventDefault()
        }}
        onDragLeave={event => {
          event.preventDefault()
          setDragging(false)
        }}
        onDrop={event => {
          event.preventDefault()
          setDragging(false)

          submitFiles(
            event.dataTransfer.files,
          )
        }}
      >
        Перетащите файлы сюда
        <br />
        или нажмите
      </div>
    </>
  )
}