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

import { BaseWidget } from "./Base"
import type { WidgetProps } from "../types"

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

export function RichTextWidget(props: WidgetProps) {
  const {
    field,
    value,
    onChange,
    loading,
  } = props

  const isMobile = window.innerWidth < 768

  return (
    <BaseWidget field={field} loading={loading}>
      {({ disabled }) => (
        <div className="ui-richtext-widget">
          <CKEditor
            editor={ClassicEditor}
            disabled={disabled}
            data={String(value || "")}
            config={{
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
                options: [
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
                ],
              },
            }}
            onChange={(
              _: EventInfo,
              editor: {
                getData: () => string
              }
            ) => {
              onChange(editor.getData())
            }}
          />
        </div>
      )}
    </BaseWidget>
  )
}