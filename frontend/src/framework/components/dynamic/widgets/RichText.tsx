import type {
  ComponentProps,
} from "react"

import { CKEditor } from "@ckeditor/ckeditor5-react"

import ClassicEditor
  from "@ckeditor/ckeditor5-build-classic"

import {
  useEffect,
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

const CompatibleClassicEditor =
  ClassicEditor as unknown as
  ComponentProps<typeof CKEditor>["editor"]

export function RichTextWidget(
  props: WidgetProps
) {
  const {
    field,
    value,
    onChange,
    loading,
  } = props

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

  const content =
    typeof value === "string"
      ? value
      : ""

  return (
    <BaseWidget
      field={field}
      loading={loading}
    >
      {({ disabled }) => {
        const readonly =
          disabled ||
          field.readonly === true

        if (readonly) {
          return (
            <article
              className="ui-richtext-readonly"
              dangerouslySetInnerHTML={{
                __html: content,
              }}
            />
          )
        }

        return (
          <div className="ui-richtext-widget">
            <CKEditor
              editor={
                CompatibleClassicEditor
              }
              data={content}
              disabled={false}
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
                onChange(
                  editor.getData()
                )
              }}
            />
          </div>
        )
      }}
    </BaseWidget>
  )
}