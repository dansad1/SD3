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
import { MetaWidget } from "./widgets/meta"
import { TimelineWidget } from "./widgets/TimelineWidget"
import { CommentWidget } from "./widgets/CommentWidget"
import { RadioWidget } from "./widgets/RadioWidget"

/* =========================================================
   TYPES
========================================================= */

export type WidgetLayout = {
    preferredSpan: number
    minSpan?: number
    maxSpan?: number
    grow?: boolean
    shrink?: boolean

}

export type WidgetDefinition = {
    component: WidgetRenderer
    aliases: string[]
    layout: WidgetLayout
}

/* =========================================================
   REGISTRY
========================================================= */

export const widgetRegistry = {

    TextInput: {
        component: TextInputWidget,

        aliases: [
            "string",
            "text",
            "textinput",
            "TextInput",
        ],

        layout: {
            preferredSpan: 6,
            grow: true,
            minSpan: 3,
            maxSpan: 12,
        },

    },


    Textarea: {

        component: TextareaWidget,

        aliases: [
            "textarea",
            "Textarea",
        ],

        layout: {
            preferredSpan: 12,
            grow: false,
        },

    },


    NumberInput: {

        component: NumberInputWidget,

        aliases: [
            "number",
            "numberinput",
            "NumberInput",
        ],

        layout: {
            preferredSpan: 4,
            grow: true,
            maxSpan: 6,
        },

    },


    Checkbox: {

        component: CheckboxWidget,

        aliases: [
            "boolean",
            "checkbox",
            "Checkbox",
        ],

        layout: {
            preferredSpan: 3,
            grow: true,
            maxSpan: 6,
        },

    },
Radio: {
    component: RadioWidget,

    aliases: [
        "radio",
        "Radio",
        "radiogroup",
        "RadioGroup",
    ],

    layout: {
        preferredSpan: 6,
        grow: true,
        minSpan: 4,
        maxSpan: 12,
    },
},

    Select: {

        component: SelectWidget,

        aliases: [
            "relation",
            "select",
            "Select",
        ],

        layout: {
            preferredSpan: 6,
            grow: true,
        },

    },


    MultiSelect: {

        component: MultiSelectWidget,

        aliases: [
            "multiselect",
            "MultiSelect",
        ],

        layout: {
            preferredSpan: 12,
            grow: false,
        },

    },


    DateInput: {

        component: DateInputWidget,

        aliases: [
            "date",
            "dateinput",
            "DateInput",
        ],

        layout: {
            preferredSpan: 4,
            grow: true,
            maxSpan: 6,
        },

    },


    DateTimeInput: {

        component: DateTimeInputWidget,

        aliases: [
            "datetime",
            "datetimeinput",
            "DateTimeInput",
        ],

        layout: {
            preferredSpan: 4,
            grow: true,
            maxSpan: 6,
        },

    },


    TimeInput: {

        component: TimeInputWidget,

        aliases: [
            "time",
            "timeinput",
            "TimeInput",
        ],

        layout: {
            preferredSpan: 4,
            grow: true,
            maxSpan: 6,
        },

    },


    FileInput: {

        component: FileInputWidget,

        aliases: [
            "file",
            "fileinput",
            "FileInput",
        ],

        layout: {
            preferredSpan: 12,
            grow: false,
        },

    },
    Comments: {

    component: CommentWidget,

    aliases: [
        "comments",
        "Comments",
        "comment",
        "Comment",
    ],

    layout: {
        preferredSpan: 12,
        grow: false,
    },

},


    PasswordInput: {

        component: PasswordInputWidget,

        aliases: [
            "password",
            "passwordinput",
            "PasswordInput",
        ],

        layout: {
            preferredSpan: 6,
            grow: true,
        },

    },


    RichText: {

        component: RichTextWidget,

        aliases: [
            "richtext",
            "richtextwidget",
            "RichText",
        ],

        layout: {
            preferredSpan: 12,
            grow: false,
        },

    },


    InsertVariables: {

        component: InsertVariablesWidget,

        aliases: [
            "insertvariables",
            "InsertVariables",
        ],

        layout: {
            preferredSpan: 12,
            grow: false,
        },

    },


    PermissionEditor: {

        component: PermissionEditorWidget,

        aliases: [
            "permission_editor",
            "PermissionEditor",
        ],

        layout: {
            preferredSpan: 12,
        },

    },


    Meta: {

        component: MetaWidget,

        aliases: [
            "meta",
            "Meta",
        ],

        layout: {
            preferredSpan: 12,
            grow: false,
        },

    },
    Timeline: {

    component: TimelineWidget,

    aliases: [
        "timeline",
        "Timeline",
        "history",
    ],

    layout: {
        preferredSpan: 12,
        grow: false,
    },

},

} satisfies Record<string, WidgetDefinition>

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