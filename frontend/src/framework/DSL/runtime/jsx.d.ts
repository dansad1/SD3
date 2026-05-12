/* eslint-disable @typescript-eslint/no-empty-object-type */

import type { DSLNode } from "./runtime"

declare global {
  namespace JSX {
    type Element = DSLNode

    /**
     * ВСЕ JSX-теги — это DSLComponent
     * → props берутся из типа компонента
     */
    interface ElementClass {}

    interface ElementAttributesProperty {
      props: {}
    }

    interface IntrinsicElements {
      /**
       * запрещаем intrinsic теги типа <div />
       * и включаем строгую проверку DSL
       */
      [tag: string]: never
    }
  }
}

export {}
