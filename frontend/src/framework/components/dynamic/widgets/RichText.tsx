import { CKEditor } from "@ckeditor/ckeditor5-react"

import {
  ClassicEditor,
  Essentials,
  Paragraph,
  Bold,
  Italic,
  Underline,
  Heading,
  List,
  Link,
  Table,
  TableToolbar,
  BlockQuote,
  Indent,
  Undo,
  SourceEditing,
  type EventInfo,
} from "ckeditor5"

import "ckeditor5/ckeditor5.css"

import {
  useEffect,
  useMemo,
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
  "sourceEditing",
  "|",
  "undo",
  "redo",
]

const headingOptions = [
  {
    model: "paragraph",
    title: "Обычный текст",
    class: "ck-heading_paragraph",
  },

  {
    model: "heading1",
    view: "h1",
    title: "Заголовок 1",
    class: "ck-heading_heading1",
  },

  {
    model: "heading2",
    view: "h2",
    title: "Заголовок 2",
    class: "ck-heading_heading2",
  },

  {
    model: "heading3",
    view: "h3",
    title: "Заголовок 3",
    class: "ck-heading_heading3",
  },
] as const

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
     CONFIG
  ========================= */

  const config = useMemo(() => {
    return {
      licenseKey: "GPL",

      plugins: [
        Essentials,
        Paragraph,
        Bold,
        Italic,
        Underline,
        Heading,
        List,
        Link,
        Table,
        TableToolbar,
        BlockQuote,
        Indent,
        Undo,
        SourceEditing,
      ],

      toolbar: isMobile
        ? mobileToolbar
        : desktopToolbar,

      placeholder: field.label
        ? `Введите: ${field.label}`
        : "Введите текст",

      table: {
        contentToolbar: [
          "tableColumn",
          "tableRow",
          "mergeTableCells",
        ],
      },

     heading: {
  options: headingOptions as any,
},
    }
  }, [
    isMobile,
    field.label,
  ])

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
            config={config}

            onChange={(
              _: EventInfo,
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