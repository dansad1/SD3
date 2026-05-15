import type { ApiPageSchema } from "@/framework/page/PageSchema"

const modules = import.meta.glob<{
  default: ApiPageSchema
}>("./**/*.tsx", { eager: true })

export const PAGES: Record<string, ApiPageSchema> = {}

for (const path in modules) {
  const mod = modules[path]

  const page = mod.default

  if (!page?.id) {
    throw new Error(`Page without id: ${path}`)
  }

  if (PAGES[page.id]) {
    throw new Error(`Duplicate page id: ${page.id}`)
  }

  PAGES[page.id] = page
  console.log("PROJECT PAGES REGISTRY")
}