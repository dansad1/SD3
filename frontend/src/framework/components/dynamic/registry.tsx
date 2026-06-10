// registry.tsx

import { CheckboxWidget } from "./widgets/Checkbox"
import { DateInputWidget } from "./widgets/DateInput"
import { DateTimeInputWidget } from "./widgets/DateTime"
import { FileInputWidget } from "./widgets/FileInput"
import { InsertVariablesWidget } from "./widgets/InsertVariablesWidget"
import { MultiSelectWidget } from "./widgets/MultiSelect"
import { NumberInputWidget } from "./widgets/NumberInput"
import { PasswordInputWidget } from "./widgets/PasswordInputWidget"
import { RichTextWidget } from "./widgets/RichText"
import { SelectWidget } from "./widgets/Select"
import { TextareaWidget } from "./widgets/Textarea"
import { TextInputWidget } from "./widgets/TextInput"
import { TimeInputWidget } from "./widgets/TimeInput"

import type {
  WidgetRenderer,
} from "./types"
import { PermissionEditorWidget } from "./widgets/PermissionEditor"

/* =========================================================
   TYPES
========================================================= */

type WidgetDefinition = {
  component: WidgetRenderer

  aliases: string[]
}

/* =========================================================
   REGISTRY
========================================================= */

export const widgetRegistry = {

  TextInput: {
    component: TextInputWidget,

    aliases: [
      "string",
      "textinput",
      "TextInput",
    ],
  },

  Textarea: {
    component: TextareaWidget,

    aliases: [
      "text",
      "textarea",
      "Textarea",
      "json",
    ],
  },

  NumberInput: {
    component: NumberInputWidget,

    aliases: [
      "number",
      "numberinput",
      "NumberInput",
    ],
  },

  Checkbox: {
    component: CheckboxWidget,

    aliases: [
      "boolean",
      "checkbox",
      "Checkbox",
    ],
  },

  Select: {
    component: SelectWidget,

    aliases: [
      "relation",
      "select",
      "Select",
    ],
  },

  MultiSelect: {
    component: MultiSelectWidget,

    aliases: [
      "multiselect",
      "MultiSelect",
    ],
  },

  DateInput: {
    component: DateInputWidget,

    aliases: [
      "date",
      "dateinput",
      "DateInput",
    ],
  },

  DateTimeInput: {
    component: DateTimeInputWidget,

    aliases: [
      "datetime",
      "datetimeinput",
      "DateTimeInput",
    ],
  },

  TimeInput: {
    component: TimeInputWidget,

    aliases: [
      "time",
      "timeinput",
      "TimeInput",
    ],
  },

  FileInput: {
    component: FileInputWidget,

    aliases: [
      "file",
      "fileinput",
      "FileInput",
    ],
  },

  PasswordInput: {
    component: PasswordInputWidget,

    aliases: [
      "password",
      "passwordinput",
      "PasswordInput",
    ],
  },

  RichText: {
    component: RichTextWidget,

    aliases: [
      "richtext",
      "richtextwidget",
      "RichText",
    ],
  },

  InsertVariables: {
    component: InsertVariablesWidget,

    aliases: [
      "insertvariables",
      "InsertVariables",
    ],
  },
  PermissionEditor: {

    component: PermissionEditorWidget,

    aliases: [
      "permission_editor",
      "PermissionEditor",
    ],

  },
} satisfies Record<
  string,
  WidgetDefinition
>

/* =========================================================
   TYPES
========================================================= */

export type WidgetKey =
  keyof typeof widgetRegistry

/* =========================================================
   RESOLVER
========================================================= */

export function resolveWidgetAlias(
  value?: string
): WidgetKey | null {

  if (!value) {
    return null
  }

  const normalized =
    value.trim()

  const keys =
    Object.keys(
      widgetRegistry
    ) as WidgetKey[]

  for (const key of keys) {

    const widget =
      widgetRegistry[key]

    if (
      widget.aliases.includes(
        normalized
      )
    ) {
      return key
    }
  }

  return null
}