// components/dynamic/widgetRegistry.ts

import type { WidgetRenderer } from "./types"
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


export const widgetRegistry: Record<string, WidgetRenderer> = {
  TextInput: TextInputWidget,
  Textarea: TextareaWidget,
  NumberInput: NumberInputWidget,
  Checkbox: CheckboxWidget,
  Select: SelectWidget,
  MultiSelect: MultiSelectWidget,
  DateTimeInput: DateTimeInputWidget,
  TimeInput: TimeInputWidget, // 👈 добавили
  FileInput: FileInputWidget,
  PasswordInput: PasswordInputWidget,
  RichText: RichTextWidget,
  DateInput: DateInputWidget,
  InsertVariables: InsertVariablesWidget,





}