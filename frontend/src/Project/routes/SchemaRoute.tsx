// src/routes/SchemaRoute.tsx

import { useParams } from "react-router-dom"

import { PAGES } from "@/Project/pages"
import { PageRenderer } from "@/framework/page/render/PageRenderer"

export default function SchemaRoute() {
  const { code } = useParams<{ code?: string }>()

  const pageCode = code ?? "login"


  const page = PAGES[pageCode]

  if (!page) {
    return <div>Страница не найдена: {pageCode}</div>
  }

  return <PageRenderer schema={page} />
}