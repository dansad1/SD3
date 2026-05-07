/* AUTO-GENERATED — DO NOT EDIT */

import { Block } from "./Block"
import { normalizeChildren } from "./runtime/children"
import type { DSLComponent } from "./runtime/types"

export type Bind<T> = T | `$${string}`
export type ContainerDSL = {
  maxWidth?: ("xs" | "sm" | "md" | "lg" | "xl") | `$${string}`
  align?: ("left" | "center" | "right") | `$${string}`
  padding?: ("none" | "sm" | "md" | "lg") | `$${string}`
}

export const Container: DSLComponent<ContainerDSL> = (props) =>
  Block(
    { __type: "container", ...props },
    normalizeChildren(props.children)
  )

export type StackDSL = {
  gap?: ("none" | "sm" | "md" | "lg") | `$${string}`
  align?: ("start" | "center" | "end" | "stretch") | `$${string}`
  variant?: ("default" | "card") | `$${string}`
}

export const Stack: DSLComponent<StackDSL> = (props) =>
  Block(
    { __type: "stack", ...props },
    normalizeChildren(props.children)
  )

export type SplitDSL = {
  ratio?: string | `$${string}`
  gap?: ("none" | "sm" | "md" | "lg") | `$${string}`
  responsive?: boolean | `$${string}`
}

export const Split: DSLComponent<SplitDSL> = (props) =>
  Block(
    { __type: "split", ...props },
    normalizeChildren(props.children)
  )

export type SectionDSL = {
  title?: string | `$${string}`
  description?: string | `$${string}`
}

export const Section: DSLComponent<SectionDSL> = (props) =>
  Block(
    { __type: "section", ...props },
    normalizeChildren(props.children)
  )

export type TabsDSL = {
  variant?: ("line" | "pills" | "segmented") | `$${string}`
  align?: ("start" | "center" | "end") | `$${string}`
  lazy?: boolean | `$${string}`
}

export const Tabs: DSLComponent<TabsDSL> = (props) =>
  Block(
    { __type: "tabs", ...props },
    normalizeChildren(props.children)
  )

export type HeadingDSL = {
  text?: string | `$${string}`
  fallback?: string | `$${string}`
  level?: 1 | 2 | 3 | 4 | `$${string}`
}

export const Heading: DSLComponent<HeadingDSL> = (props) =>
  Block(
    { __type: "heading", ...props },
    normalizeChildren(props.children)
  )

export type TextDSL = {
  value?: string | `$${string}`
  muted?: boolean | `$${string}`
}

export const Text: DSLComponent<TextDSL> = (props) =>
  Block(
    { __type: "text", ...props },
    normalizeChildren(props.children)
  )

export type DividerDSL = Record<string, never>

export const Divider: DSLComponent<DividerDSL> = (props) =>
  Block(
    { __type: "divider", ...props },
    normalizeChildren(props.children)
  )

export type SpacerDSL = {
  size?: number | `$${string}`
}

export const Spacer: DSLComponent<SpacerDSL> = (props) =>
  Block(
    { __type: "spacer", ...props },
    normalizeChildren(props.children)
  )

export type BadgeDSL = {
  label?: string | `$${string}`
  color?: ("default" | "success" | "warning" | "danger") | `$${string}`
  size?: ("sm" | "md" | "lg") | `$${string}`
}

export const Badge: DSLComponent<BadgeDSL> = (props) =>
  Block(
    { __type: "badge", ...props },
    normalizeChildren(props.children)
  )

export type Insert_variablesDSL = {
  source?: string | `$${string}`
  targetField?: string | `$${string}`
  title?: string | `$${string}`
  format?: ("template" | "raw" | "dollar") | `$${string}`
}

export const Insert_variables: DSLComponent<Insert_variablesDSL> = (props) =>
  Block(
    { __type: "insert_variables", ...props },
    normalizeChildren(props.children)
  )

export type ActionDSL = {
  label?: string | `$${string}`
  icon?: string | `$${string}`
  to?: string | `$${string}`
  action?: string | `$${string}`
  ctx?: Record<string, unknown> | `$${string}`
  variant?: ("primary" | "secondary" | "ghost" | "danger") | `$${string}`
}

export const Action: DSLComponent<ActionDSL> = (props) =>
  Block(
    { __type: "action", ...props },
    normalizeChildren(props.children)
  )

export type LinkDSL = {
  label?: string | `$${string}`
  to?: string | `$${string}`
  external?: boolean | `$${string}`
}

export const Link: DSLComponent<LinkDSL> = (props) =>
  Block(
    { __type: "link", ...props },
    normalizeChildren(props.children)
  )

export type UploadDSL = {
  name?: string | `$${string}`
  label?: string | `$${string}`
  multiple?: boolean | `$${string}`
  upload_action?: string | `$${string}`
  commit_action?: string | `$${string}`
  files?: unknown[] | `$${string}`
  ctx?: Record<string, unknown> | `$${string}`
  refresh?: unknown[] | `$${string}`
  accept?: string | `$${string}`
  auto_commit?: boolean | `$${string}`
  disabled?: boolean | `$${string}`
}

export const Upload: DSLComponent<UploadDSL> = (props) =>
  Block(
    { __type: "upload", ...props },
    normalizeChildren(props.children)
  )

export type IfDSL = {
  when?: string | `$${string}`
}

export const If: DSLComponent<IfDSL> = (props) => ({
  __dsl: "control",
  type: "if",
  props,
  children: normalizeChildren(props.children),
})

export type ForDSL = {
  each?: string | `$${string}`
  range?: number | `$${string}`
  as?: string | `$${string}`
  index?: string | `$${string}`
}

export const For: DSLComponent<ForDSL> = (props) => ({
  __dsl: "control",
  type: "for",
  props,
  children: normalizeChildren(props.children),
})

export type ResourceDSL = {
  source?: string | `$${string}`
  params?: Record<string, unknown> | `$${string}`
  assign?: string | `$${string}`
  lazy?: boolean | `$${string}`
  watch?: unknown[] | `$${string}`
}

export const Resource: DSLComponent<ResourceDSL> = (props) =>
  Block(
    { __type: "resource", ...props },
    normalizeChildren(props.children)
  )

export type CustomDSL = {
  component?: string | `$${string}`
  props?: Record<string, unknown> | `$${string}`
}

export const Custom: DSLComponent<CustomDSL> = (props) =>
  Block(
    { __type: "custom", ...props },
    normalizeChildren(props.children)
  )

export type FormDSL =
  (({
  entity: string | `$${string}`
  mode?: ("create" | "edit" | "view") | `$${string}`
  objectId?: string | `$${string}`
  initial?: Record<string, unknown> | `$${string}`
  submit?: {
  label?: string | `$${string}`
  action?: string | `$${string}`
  redirect?: (string | `$${string}` | {
  to?: string | `$${string}`
  ctx?: Record<string, unknown> | `$${string}`
}) | `$${string}`
  closeModal?: boolean | `$${string}`
}
} | {
  schema: string | `$${string}`
  submit: (string | `$${string}` | {
  action?: string | `$${string}`
  label?: string | `$${string}`
  redirect?: (string | `$${string}` | {
  to?: string | `$${string}`
  ctx?: Record<string, unknown> | `$${string}`
}) | `$${string}`
  closeModal?: boolean | `$${string}`
}) | `$${string}`
  redirect?: (string | `$${string}` | {
  to?: string | `$${string}`
  ctx?: Record<string, unknown> | `$${string}`
}) | `$${string}`
}) & {
  formLayout?: {
  preset?: ("default" | "two-columns" | "single-column" | "wide") | `$${string}`
  density?: ("comfortable" | "default" | "compact" | "dense") | `$${string}`
}
}) & { children?: unknown }

export const Form: DSLComponent<FormDSL> = (props) =>
  Block(
    { __type: "form", ...props },
    normalizeChildren(props.children)
  )

export type TableDSL = {
  entity?: string | `$${string}`
  fieldset?: string | `$${string}`
  data?: unknown
  filter?: Record<string, unknown> | `$${string}`
  searchableFields?: unknown[] | `$${string}`
  selectionActions?: unknown[] | `$${string}`
  rowClick?: (boolean | `$${string}` | {
  to?: string | `$${string}`
  action?: string | `$${string}`
  params?: Record<string, unknown> | `$${string}`
  ctx?: Record<string, unknown> | `$${string}`
  confirm?: (boolean | `$${string}` | {
  message?: string | `$${string}`
}) | `$${string}`
}) | `$${string}`
  to?: string | `$${string}`
  features?: {
  toolbar?: boolean | `$${string}`
  search?: boolean | `$${string}`
  selection?: boolean | `$${string}`
  rowClick?: boolean | `$${string}`
  rowActions?: boolean | `$${string}`
  visibleFields?: boolean | `$${string}`
}
  toolbar?: {
  actions?: unknown[] | `$${string}`
}
  rowActions?: unknown[] | `$${string}`
  bulkActions?: unknown[] | `$${string}`
}

export const Table: DSLComponent<TableDSL> = (props) =>
  Block(
    { __type: "table", ...props },
    normalizeChildren(props.children)
  )

export type MatrixDSL = {
  source?: string | `$${string}`
  params?: Record<string, unknown> | `$${string}`
}

export const Matrix: DSLComponent<MatrixDSL> = (props) =>
  Block(
    { __type: "matrix", ...props },
    normalizeChildren(props.children)
  )

export type Chat_threadDSL = {
  thread?: unknown
  participants?: unknown[] | `$${string}`
  messages?: unknown[] | `$${string}`
  currentUserId?: string | `$${string}`
  reply?: {
  schema?: string | `$${string}`
  submit?: {
  action?: string | `$${string}`
  label?: string | `$${string}`
  redirect?: (string | `$${string}` | {
  to?: string | `$${string}`
  ctx?: Record<string, unknown> | `$${string}`
}) | `$${string}`
  closeModal?: boolean | `$${string}`
}
  ctx?: Record<string, unknown> | `$${string}`
}
  features?: {
  header?: boolean | `$${string}`
  participants?: boolean | `$${string}`
  timestamps?: boolean | `$${string}`
  grouping?: boolean | `$${string}`
  autoScroll?: boolean | `$${string}`
  realtime?: boolean | `$${string}`
  attachments?: boolean | `$${string}`
}
}

export const Chat_thread: DSLComponent<Chat_threadDSL> = (props) =>
  Block(
    { __type: "chat_thread", ...props },
    normalizeChildren(props.children)
  )

export type Chat_listDSL = {
  data?: unknown[] | `$${string}`
  selectedId?: string | `$${string}`
  to?: string | `$${string}`
  features?: {
  unread?: boolean | `$${string}`
  timestamp?: boolean | `$${string}`
}
}

export const Chat_list: DSLComponent<Chat_listDSL> = (props) =>
  Block(
    { __type: "chat_list", ...props },
    normalizeChildren(props.children)
  )

