/// <reference types="node" />

import fs from "fs"
import path from "path"
import { fileURLToPath } from "url"
import { Registry } from "../language"

/* =========================================================
   TYPES
========================================================= */

type BlockDef = Record<string, unknown>
type RegistryGroup = Record<string, BlockDef>

/* ===================== paths ===================== */

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
const OUT = path.resolve(
  __dirname,
  "../blocks.generated.ts"
)

/* ===================== helpers ===================== */

function capitalize(name: string) {
  return name.charAt(0).toUpperCase() + name.slice(1)
}

function bindable(type: string) {
  return `${type} | \`$\${string}\``
}

function isPrimitiveKeyword(v: string) {
  return (
    v === "string" ||
    v === "number" ||
    v === "boolean" ||
    v === "array" ||
    v === "object" ||
    v === "any"
  )
}

function asRecord(
  value: unknown
): Record<string, unknown> {
  if (
    typeof value === "object" &&
    value !== null &&
    !Array.isArray(value)
  ) {
    return value as Record<string, unknown>
  }

  return {}
}

/* =========================================================
   TYPE SYSTEM
========================================================= */

function genObjectShape(
  props: Record<string, unknown>,
  forceOptional = true
): string {
  const entries = Object.entries(props)

  if (entries.length === 0) {
    return "Record<string, never>"
  }

  return `{
${entries
  .map(([rawKey, v]) => {
    const explicitOptional = rawKey.endsWith("?")
    const key = explicitOptional
      ? rawKey.slice(0, -1)
      : rawKey

    const optional =
      forceOptional || explicitOptional

    return `  ${key}${optional ? "?" : ""}: ${tsType(v)}`
  })
  .join("\n")}
}`
}

function tsType(spec: unknown): string {
  if (Array.isArray(spec)) {
    if (spec.every(v => typeof v === "number")) {
      return bindable(spec.join(" | "))
    }

    const union = spec
      .map(v => {
        if (
          typeof v === "object" &&
          v !== null &&
          !Array.isArray(v)
        ) {
          return genObjectShape(
            v as Record<string, unknown>,
            true
          )
        }

        if (typeof v === "string") {
          if (isPrimitiveKeyword(v)) {
            return tsType(v)
          }

          return `"${v}"`
        }

        return String(v)
      })
      .join(" | ")

    return bindable(`(${union})`)
  }

  if (spec === "string") {
    return bindable("string")
  }

  if (spec === "number") {
    return bindable("number")
  }

  if (spec === "boolean") {
    return bindable("boolean")
  }

  if (spec === "array") {
    return bindable("unknown[]")
  }

  if (spec === "object") {
    return bindable("Record<string, unknown>")
  }

  if (spec === "any") {
    return "unknown"
  }

  if (
    typeof spec === "object" &&
    spec !== null
  ) {
    return genObjectShape(
      spec as Record<string, unknown>,
      true
    )
  }

  return "unknown"
}

function genModesUnion(
  modes: Record<string, Record<string, unknown>>,
  discriminator: string | false = "type"
) {
  return Object.entries(modes)
    .map(([modeName, modeProps]) => {
      const body = Object.entries(modeProps)
        .map(([rawKey, v]) => {
          const explicitOptional =
            rawKey.endsWith("?")

          const key = explicitOptional
            ? rawKey.slice(0, -1)
            : rawKey

          return `  ${key}${explicitOptional ? "?" : ""}: ${tsType(v)}`
        })
        .join("\n")

      const discLine = discriminator
        ? `  ${discriminator}: "${modeName}"\n`
        : ""

      return `{
${discLine}${body ? body + "\n" : ""}}`
    })
    .join(" | ")
}

/* =========================================================
   FLATTEN
========================================================= */

function flattenContentProps(
  def: BlockDef
): Record<string, unknown> {
  const out: Record<string, unknown> = {}

  if (
    def.props &&
    typeof def.props === "object" &&
    !Array.isArray(def.props)
  ) {
    Object.assign(out, def.props)
  }

  for (const [k, v] of Object.entries(def)) {
    if (k === "props" || k === "modes") {
      continue
    }

    out[k] = v
  }

  return out
}

/* =========================================================
   GENERATORS
========================================================= */

function genSimpleBlock(
  name: string,
  props: Record<string, unknown>
) {
  const Fn = capitalize(name)
  const propsType = genObjectShape(props)

  return `
export type ${Fn}DSL = ${propsType}

export const ${Fn}: DSLComponent<${Fn}DSL> = (props) =>
  Block(
    { __type: "${name}", ...props },
    normalizeChildren(props.children)
  )
`
}

function genControlBlock(
  name: string,
  props: Record<string, unknown>
) {
  const Fn = capitalize(name)
  const propsType = genObjectShape(props)

  return `
export type ${Fn}DSL = ${propsType}

export const ${Fn}: DSLComponent<${Fn}DSL> = (props) => ({
  __dsl: "control",
  type: "${name}",
  props,
  children: normalizeChildren(props.children),
})
`
}

function genContentBlock(
  name: string,
  def: BlockDef
) {
  const Fn = capitalize(name)

  if (
    def.modes &&
    typeof def.modes === "object" &&
    !Array.isArray(def.modes)
  ) {
    const union = genModesUnion(
      def.modes as Record<
        string,
        Record<string, unknown>
      >,
      name === "form" ? false : "type"
    )

    const sharedProps =
      flattenContentProps(def)

    const sharedType =
      Object.keys(sharedProps).length > 0
        ? ` & ${genObjectShape(sharedProps, true)}`
        : ""

    return `
export type ${Fn}DSL =
  ((${union})${sharedType}) & { children?: unknown }

export const ${Fn}: DSLComponent<${Fn}DSL> = (props) =>
  Block(
    { __type: "${name}", ...props },
    normalizeChildren(props.children)
  )
`
  }

  return genSimpleBlock(
    name,
    flattenContentProps(def)
  )
}

/* =========================================================
   HEADER
========================================================= */

let code = `
/* AUTO-GENERATED — DO NOT EDIT */

import { Block } from "./Block"
import { normalizeChildren } from "./runtime/children"
import type { DSLComponent } from "./runtime/types"

export type Bind<T> = T | \`$\${string}\`
`.trim()

/* =========================================================
   REGISTRY
========================================================= */

function generateSimpleGroup(
  group: RegistryGroup
) {
  for (const [name, def] of Object.entries(group)) {
    code += genSimpleBlock(
      name,
      asRecord(def.props)
    )
  }
}

function generateControlGroup(
  group: RegistryGroup
) {
  for (const [name, def] of Object.entries(group)) {
    code += genControlBlock(
      name,
      asRecord(def.props)
    )
  }
}

/* =========================
   GROUPS
========================= */

generateSimpleGroup(
  Registry.structural as RegistryGroup
)

generateSimpleGroup(
  Registry.atom as RegistryGroup
)

generateSimpleGroup(
  Registry.action as RegistryGroup
)

if ("control" in Registry) {
  generateControlGroup(
    Registry.control as RegistryGroup
  )
}

if ("data" in Registry) {
  generateSimpleGroup(
    Registry.data as RegistryGroup
  )
}

for (const [name, def] of Object.entries(
  Registry.content as RegistryGroup
)) {
  code += genContentBlock(name, def)
}

/* =========================================================
   WRITE
========================================================= */

const next = code + "\n"

let prev = ""

if (fs.existsSync(OUT)) {
  prev = fs.readFileSync(OUT, "utf-8")
}

/* 👉 не перезаписываем если нет изменений */
if (prev === next) {
  console.log("✔ DSL unchanged:", OUT)
} else {
  fs.writeFileSync(OUT, next, { flag: "w" })

  console.log("✔ DSL blocks generated:", OUT)
}