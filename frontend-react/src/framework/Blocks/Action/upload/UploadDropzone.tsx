import { useRef } from "react"

export function UploadDropzone({
  onFiles,
  disabled,
  multiple,
  accept,
}: {
  onFiles: (files: File[]) => void
  disabled?: boolean
  multiple?: boolean
  accept?: string
}) {
  const inputRef = useRef<HTMLInputElement>(null)

  const open = () => {
    if (disabled) return
    inputRef.current?.click()
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
        onChange={e =>
          onFiles(Array.from(e.target.files || []))
        }
      />

      <div
        className={`upload__dropzone ${
          disabled ? "is-disabled" : ""
        }`}
        onClick={open}
      >
        Перетащите файлы или нажмите
      </div>
    </>
  )
}