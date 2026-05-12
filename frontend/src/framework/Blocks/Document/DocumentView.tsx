// DocumentView.tsx

import { CKEditor } from "@ckeditor/ckeditor5-react"

import ClassicEditor
  from "@ckeditor/ckeditor5-build-classic"

import type { DocumentVM } from "./types"

export function DocumentView({
  loading,
  saving,

  content,

  editable,

  fullscreen,

  setContent,

  save,
}: DocumentVM) {

  if (loading) {
    return (
      <div>
        loading...
      </div>
    )
  }

  return (
    <div
      style={{
        width: "100%",
        height: fullscreen
          ? "100vh"
          : undefined,
      }}
    >

      <CKEditor
        editor={ClassicEditor}
        disabled={!editable}
        data={content}

        onChange={(_, editor) => {
          setContent(
            editor.getData()
          )
        }}
      />

      {
        editable && (
          <div
            style={{
              marginTop: 16,
            }}
          >

            <button
              disabled={saving}
              onClick={() => {
                save()
              }}
            >
              {
                saving
                  ? "Сохранение..."
                  : "Сохранить"
              }
            </button>

          </div>
        )
      }

    </div>
  )
}