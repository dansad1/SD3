import type {
  ComponentProps,
  CSSProperties,
} from "react"


import { CKEditor } from "@ckeditor/ckeditor5-react"

import ClassicEditor
  from "@ckeditor/ckeditor5-build-classic"

import type {
  DocumentToolbar,
  DocumentVM,
} from "./types"

/*
 * Временный адаптер типов.
 *
 * Он нужен, когда runtime-версии CKEditor совместимы,
 * но декларации типов установленных пакетов расходятся.
 *
 * Пакеты всё равно следует выровнять по версиям.
 */
const CompatibleClassicEditor =
  ClassicEditor as unknown as
  ComponentProps<typeof CKEditor>["editor"]

const toolbarItems: Record<
  DocumentToolbar,
  string[]
> = {
  minimal: [
    "bold",
    "italic",
    "link",
    "undo",
    "redo",
  ],

  compact: [
    "heading",
    "bold",
    "italic",
    "link",
    "bulletedList",
    "numberedList",
    "undo",
    "redo",
  ],

  full: [
    "heading",
    "|",
    "bold",
    "italic",
    "link",
    "bulletedList",
    "numberedList",
    "blockQuote",
    "|",
    "undo",
    "redo",
  ],
}

const rootStyle: CSSProperties = {
  width: "100%",
}

const errorStyle: CSSProperties = {
  padding: 12,
  marginBottom: 16,
  border: "1px solid currentColor",
  borderRadius: 4,
}



export function DocumentView({
  loading,
  saving,
  error,

  content,

  mode,
  editable,
  toolbar,
  fullscreen,

  setContent,
  save,
}: DocumentVM) {
  if (loading) {
    return (
      <div>
        Загрузка документа...
      </div>
    )
  }

  const containerStyle: CSSProperties = {
    ...rootStyle,
    height: fullscreen
      ? "100vh"
      : undefined,
    overflow: fullscreen
      ? "auto"
      : undefined,
  }

 if (mode === "read") {
  return (
    <div style={containerStyle}>
      {error && (
        <div role="alert">
          {error}
        </div>
      )}

      <article
        style={{
          whiteSpace: "pre-wrap",
          overflowWrap: "anywhere",
          lineHeight: 1.6,
        }}
      >
        {content}
      </article>
    </div>
  )
}

  return (
    <div style={containerStyle}>
      {error && (
        <div
          role="alert"
          style={errorStyle}
        >
          {error}
        </div>
      )}

      <CKEditor
        editor={CompatibleClassicEditor}
        disabled={!editable}
        data={content}
        config={{
          toolbar: {
            items: toolbarItems[toolbar],
          },
        }}
        onChange={(_, editor) => {
          setContent(editor.getData())
        }}
      />

      {editable && (
        <div
          style={{
            marginTop: 16,
          }}
        >
          <button
            type="button"
            disabled={saving}
            onClick={() => {
              void save().catch(() => {
                /*
                 * Ошибка отображается через error.
                 */
              })
            }}
          >
            {saving
              ? "Сохранение..."
              : "Сохранить"}
          </button>
        </div>
      )}
    </div>
  )
}