import type { DSLNode } from "../runtime"

/**
 * Один child:
 * поддерживаем JSX-условия
 */
export type DSLChild =
  | DSLNode
  | null
  | undefined
  | false

/**
 * Children:
 * один или массив
 */
export type DSLChildren =
  | DSLChild
  | DSLChild[]

/**
 * DSL компонент
 */
export type DSLComponent<P = object> = (
  props: P & { children?: DSLChildren }
) => DSLNode