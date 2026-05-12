/// <reference types="node" />

import {
  Project,
  Node,
  SyntaxKind,
  SourceFile,
  ObjectLiteralExpression,
} from "ts-morph"

import * as fs from "fs"
import * as path from "path"
import { execSync } from "child_process"

/* ===================================================== */
/* CONFIG */
/* ===================================================== */

const args = process.argv.slice(2)

const name = args[0]

const isComplex =
  args.includes("complex") ||
  args.includes("--complex")

if (!name) {
  fail("Usage: generate-block <name> [complex]")
}

const pascal = capitalize(name)

const project = new Project({
  skipAddingFilesFromTsConfig: true,
})

/* ===================================================== */
/* PATHS */
/* ===================================================== */

const PATH_LANGUAGE = "src/framework/DSL/language.ts"
const PATH_PAGE_SCHEMA = "src/framework/page/PageSchema.ts"
const PATH_NORMALIZE_DISPATCH =
  "src/framework/normalize/normalizeDispatch.ts"

const BLOCKS_ROOT = "src/framework/Blocks"

const KIND_DIR = {
  structural: "Structural",
  atom: "Atom",
  action: "Action",
  control: "Control",
  content: "Content",
} as const

type BlockKind = keyof typeof KIND_DIR

/* ===================================================== */
/* MAIN */
/* ===================================================== */

async function run() {
  /* 1. пересобираем DSL */
  execSync("npm run dsl:gen", { stdio: "inherit" })

  project.addSourceFileAtPath(PATH_LANGUAGE)
  project.addSourceFileAtPath(PATH_PAGE_SCHEMA)
  project.addSourceFileAtPath(PATH_NORMALIZE_DISPATCH)

  const languageFile =
    project.getSourceFileOrThrow(PATH_LANGUAGE)

  const resolved = resolveBlockFromLanguage(
    languageFile,
    name
  )

  if (!resolved) {
    fail(`Block "${name}" not found in language.ts`)
  }

  const isAtom = resolved.kind === "atom"

  const baseDir = path.join(
    BLOCKS_ROOT,
    KIND_DIR[resolved.kind]
  )

  const dir = isAtom
    ? baseDir
    : path.join(baseDir, pascal)

  fs.mkdirSync(dir, { recursive: true })

  /* ---------- generate ---------- */

  if (isAtom) {
    ensureAtom(dir)
    ensureAtomTypes(dir, resolved.blockNode)
  } else {
    ensureBlock(dir)
    ensureTypes(dir, resolved.blockNode)
    ensureNormalize(dir)
    ensureRegister(dir)

    if (isComplex) {
      ensureView(dir)
      ensureController(dir)

      if (hasLogic(resolved.blockNode)) {
        ensureEngine(dir)
      }
    }
  }

  /* 🔥 ВАЖНЫЙ ПОРЯДОК */
  updatePageSchemaUnion()
  updateNormalizeDispatch(resolved.kind, isAtom)

  await project.save()

  execSync("npx tsc --noEmit", { stdio: "inherit" })

  console.log("✔ Block generated:", name)
}

void run()

/* ===================================================== */
/* GENERATORS */
/* ===================================================== */

function ensureAtom(dir: string) {
  writeFile(
    path.join(dir, `${pascal}Block.tsx`),
    `import type { ${pascal}Block } from "./types"

export function ${pascal}Block({ block }: { block: ${pascal}Block }) {
  return <div>${pascal}</div>
}
`
  )
}

function ensureAtomTypes(
  dir: string,
  node: ObjectLiteralExpression
) {
  const fields = extractFields(node)

  writeFile(
    path.join(dir, "types.ts"),
    `import type { BaseBlock } from "../BlockType"

export type ${pascal}Block = BaseBlock & {
  type: "${name}"
  ${fields.join("\n  ")}
}
`
  )
}

function ensureBlock(dir: string) {
  writeFile(
    path.join(dir, `${pascal}Block.tsx`),
    `import type { ${pascal}Block } from "./types"
import { use${pascal}Controller } from "./use${pascal}Controller"
import { ${pascal}View } from "./${pascal}View"

export function ${pascal}Block({ block }: { block: ${pascal}Block }) {
  const vm = use${pascal}Controller(block)
  return <${pascal}View {...vm} />
}
`
  )
}

function ensureController(dir: string) {
  writeFile(
    path.join(dir, `use${pascal}Controller.ts`),
    `import { resolveProps } from "@/framework/bind/expression/resolveProps"
import { usePageRuntimeContext } from "@/framework/page/runtime/usePageRuntimeContext"
import type { ${pascal}Block } from "./types"

export function use${pascal}Controller(block: ${pascal}Block) {
  const ctx = usePageRuntimeContext() as Record<string, unknown>
  return resolveProps(block as Record<string, unknown>, ctx)
}
`
  )
}

function ensureView(dir: string) {
  writeFile(
    path.join(dir, `${pascal}View.tsx`),
    `export function ${pascal}View(props: Record<string, unknown>) {
  return <div>${pascal} view</div>
}
`
  )
}

function ensureEngine(dir: string) {
  writeFile(
    path.join(dir, `${name}Engine.ts`),
    `export function build${pascal}(input: Record<string, unknown>) {
  return input
}
`
  )
}

function ensureTypes(
  dir: string,
  node: ObjectLiteralExpression
) {
  const fields = extractFields(node)

  writeFile(
    path.join(dir, "types.ts"),
    `import type { BaseBlock } from "../../BlockType"

export type ${pascal}Block = BaseBlock & {
  type: "${name}"
  ${fields.join("\n  ")}
}
`
  )
}

function ensureNormalize(dir: string) {
  writeFile(
    path.join(dir, "normalize.ts"),
    `import { normalizeId } from "@/framework/normalize/normalizeCommon"
import type { ApiPageBlock } from "@/framework/page/PageSchema"

type Api = Extract<ApiPageBlock, { type: "${name}" }>

export function normalize${pascal}(block: Api): Api {
  return {
    ...block,
    id: normalizeId(block.id),
  }
}
`
  )
}



function ensureRegister(dir: string) {
  writeFile(
    path.join(dir, "register.ts"),
    `import { blockRegistry } from "@/framework/Blocks/Registry/BlockRegistry"
import { ${pascal}Block } from "./${pascal}Block"

export {}

blockRegistry.register("${name}", ${pascal}Block)
`
  )
}

/* ===================================================== */
/* NORMALIZE DISPATCH */
/* ===================================================== */

function updateNormalizeDispatch(
  kind: BlockKind,
  isAtom: boolean
) {
  if (isAtom) return

  const file =
    project.getSourceFileOrThrow(
      PATH_NORMALIZE_DISPATCH
    )

  const fnName = `normalize${pascal}`
  const importPath = `../Blocks/${KIND_DIR[kind]}/${pascal}/normalize`

  /* import */

  const hasImport = file
    .getImportDeclarations()
    .some(
      d =>
        d.getModuleSpecifierValue() === importPath &&
        d
          .getNamedImports()
          .some(n => n.getName() === fnName)
    )

  if (!hasImport) {
    file.addImportDeclaration({
      namedImports: [fnName],
      moduleSpecifier: importPath,
    })
  }

  /* normalizeMap */

  const varDecl = file
    .getVariableDeclarations()
    .find(v => v.getName() === "normalizeMap")

  if (!varDecl) {
    console.warn("normalizeMap not found")
    return
  }

  const init = varDecl.getInitializer()

  if (!init || !Node.isObjectLiteralExpression(init)) {
    console.warn("normalizeMap is not object")
    return
  }

  const exists = init
    .getProperties()
    .some(
      p =>
        Node.isPropertyAssignment(p) &&
        p.getName().replace(/['"]/g, "") === name
    )

  if (!exists) {
    init.addPropertyAssignment({
      name,
      initializer: fnName,
    })
  }
}
function getImportPath(): string {
  const languageFile =
    project.getSourceFileOrThrow(PATH_LANGUAGE)

  const resolved = resolveBlockFromLanguage(
    languageFile,
    name
  )

  if (!resolved) {
    fail("Cannot resolve import path")
  }

  if (resolved.kind === "atom") {
    return `../Blocks/${KIND_DIR[resolved.kind]}/types`
  }

  return `../Blocks/${KIND_DIR[resolved.kind]}/${pascal}/types`
}

/* ===================================================== */
/* PAGE SCHEMA */
/* ===================================================== */

function updatePageSchemaUnion() {
  const file =
    project.getSourceFileOrThrow(
      PATH_PAGE_SCHEMA
    )

  const union =
    file.getTypeAlias("ApiPageBlock")

  if (!union) return

  const typeName = `${pascal}Block`
  const current =
    union.getTypeNodeOrThrow().getText()

  /* ---------- UNION ---------- */

  if (!current.includes(typeName)) {
    union.setType(`${current} | ${typeName}`)
  }

  /* ---------- IMPORT ---------- */

  const importPath = getImportPath()

  const alreadyImported = file
    .getImportDeclarations()
    .some(
      d =>
        d.getModuleSpecifierValue() === importPath &&
        d
          .getNamedImports()
          .some(n => n.getName() === typeName)
    )

  if (!alreadyImported) {
    file.addImportDeclaration({
      namedImports: [typeName],
      moduleSpecifier: importPath,
      isTypeOnly: true,
    })
  }
}
/* ===================================================== */
/* DSL PARSE */
/* ===================================================== */

function resolveBlockFromLanguage(
  file: SourceFile,
  blockName: string
): {
  kind: BlockKind
  blockNode: ObjectLiteralExpression
} | null {
  const groups = [
    { kind: "structural", exportName: "Structural" },
    { kind: "atom", exportName: "Atom" },
    { kind: "action", exportName: "Action" },
    { kind: "control", exportName: "Control" },
    { kind: "content", exportName: "Content" },
  ] as const

  for (const group of groups) {
    const decl = file.getVariableDeclaration(
      group.exportName
    )
    if (!decl) continue

    const init = decl.getInitializer()
    if (!init) continue

    const obj = Node.isObjectLiteralExpression(init)
      ? init
      : Node.isAsExpression(init)
      ? init.getExpression()
      : null

    if (!obj || !Node.isObjectLiteralExpression(obj))
      continue

    for (const prop of obj.getProperties()) {
      if (!Node.isPropertyAssignment(prop))
        continue

      const key = prop.getName().replace(/['"]/g, "")

      if (key === blockName) {
        return {
          kind: group.kind,
          blockNode:
            prop.getInitializerIfKindOrThrow(
              SyntaxKind.ObjectLiteralExpression
            ),
        }
      }
    }
  }

  return null
}

/* ===================================================== */
/* FIELDS */
/* ===================================================== */
function resolveTsType(node: Node): string {
  if (Node.isStringLiteral(node)) {
    const v = node.getLiteralText()

    if (v === "string") return "string | `$${string}`"
    if (v === "number") return "number | `$${string}`"
    if (v === "boolean") return "boolean | `$${string}`"

    return `"${v}"`
  }

  if (Node.isArrayLiteralExpression(node)) {
    const values = node.getElements().map(el => {
      if (Node.isStringLiteral(el)) {
        return `"${el.getLiteralText()}"`
      }
      return el.getText()
    })

    return values.join(" | ")
  }

  if (Node.isObjectLiteralExpression(node)) {
    return `{
${node
  .getProperties()
  .filter(Node.isPropertyAssignment)
  .map(p => {
    const key = p.getName()
    const val = p.getInitializer()
    if (!val) return ""

    return `  ${key}: ${resolveTsType(val)}`
  })
  .join("\n")}
}`
  }

  return "any"
}
function extractFields(
  node: ObjectLiteralExpression
): string[] {
  const props = node.getProperty("props")

  if (!props || !Node.isPropertyAssignment(props)) {
    return []
  }

  const init = props.getInitializer()

  if (!init || !Node.isObjectLiteralExpression(init)) {
    return []
  }

  const out: string[] = []

  for (const p of init.getProperties()) {
    if (!Node.isPropertyAssignment(p)) continue

    const key = p.getName()
    const value = p.getInitializer()

    if (!value) continue

    const tsType = resolveTsType(value)

    out.push(`${key}: ${tsType}`)
  }

  return out
}

/* ===================================================== */
/* UTILS */
/* ===================================================== */

function writeFile(file: string, content: string) {
  if (!fs.existsSync(file)) {
    fs.writeFileSync(file, content)
  }
}

function hasLogic(node: ObjectLiteralExpression) {
  const t = node.getText()
  return t.includes("each") || t.includes("when")
}

function capitalize(x: string) {
  return x.charAt(0).toUpperCase() + x.slice(1)
}

function fail(msg: string): never {
  console.error(msg)
  process.exit(1)
  throw new Error(msg)
}