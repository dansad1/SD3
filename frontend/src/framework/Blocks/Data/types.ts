// src/framework/Blocks/Data/types.ts

import type { PageBlock } from "@/framework/page/PageSchema"
import type { BaseBlock } from "../BlockType"

export type ResourceBlock = BaseBlock & {
  type: "resource"

  /**
   * Код ресурса (backend)
   * /resource/{source}
   */
  source: string

  /**
   * Параметры запроса
   * поддерживают bind:
   *   { group_id: "$query.group_id" }
   */
  params?: Record<string, unknown>

  /**
   * Куда положить результат в PageContext.data
   * потом доступно как:
   *   $stats
   *   $data.stats
   */
  assign: string

  /**
   * Не грузить сразу
   */
  lazy?: boolean

  /**
   * 🔥 зависимости (bind-aware)
   * при изменении → рефетч
   *
   * пример:
   *   ["$query.group_id", "$form.values.date"]
   */
  watch?: string[]

  /**
   * Вложенные блоки (Table, Form и т.д.)
   */
  blocks: PageBlock[]
}