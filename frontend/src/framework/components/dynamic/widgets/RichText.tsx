import { CKEditor } from "@ckeditor/ckeditor5-react"

import ClassicEditor
  from "@ckeditor/ckeditor5-build-classic"

import {
  useEffect,
  useRef,
  useState,
} from "react"

import { BaseWidget } from "./Base"

import type { WidgetProps } from "../types"

const MOBILE_BREAKPOINT = 768

const mobileToolbar = [
  "bold",
  "italic",
  "|",
  "bulletedList",
  "numberedList",
  "|",
  "link",
  "|",
  "undo",
  "redo",
]

const desktopToolbar = [
  "heading",
  "|",
  "bold",
  "italic",
  "underline",
  "|",
  "bulletedList",
  "numberedList",
  "outdent",
  "indent",
  "|",
  "link",
  "insertTable",
  "blockQuote",
  "|",
  "undo",
  "redo",
]

export function RichTextWidget(
  props: WidgetProps
) {
  const {
    field,
    value,
    onChange,
    loading,
  } = props

  /* =========================
     MOBILE
  ========================= */

  const [isMobile, setIsMobile] =
    useState(false)

  useEffect(() => {
    if (
      typeof window ===
      "undefined"
    ) {
      return
    }

    const update = () => {
      setIsMobile(
        window.innerWidth <
          MOBILE_BREAKPOINT
      )
    }

    update()

    window.addEventListener(
      "resize",
      update
    )

    return () => {
      window.removeEventListener(
        "resize",
        update
      )
    }
  }, [])

  /* =========================
     LOCAL STATE
  ========================= */

  const [localValue, setLocalValue] =
    useState(
      String(value || "")
    )

  const isInternalChange =
    useRef(false)

  useEffect(() => {
    if (
      isInternalChange.current
    ) {
      isInternalChange.current =
        false

      return
    }

    setLocalValue(
      String(value || "")
    )
  }, [value])

  /* =========================
     RENDER
  ========================= */

  return (
    <BaseWidget
      field={field}
      loading={loading}
    >
      {({ disabled }) => (
        <div className="ui-richtext-widget">

          <CKEditor
            editor={ClassicEditor}

            disabled={disabled}

            data={localValue}

            config={{
              toolbar: isMobile
                ? mobileToolbar
                : desktopToolbar,

              placeholder: field.label
                ? `Введите: ${field.label}`
                : "Введите текст",
            }}

            onChange={(
              _,
              editor
            ) => {
              const html =
                editor.getData()

              isInternalChange.current =
                true

              setLocalValue(html)

              onChange(html)
            }}
          />

        </div>
      )}
    </BaseWidget>
  )
}