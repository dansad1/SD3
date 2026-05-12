import type { FC } from "react"
import type { Platform, PresentationNode, RenderContext } from "../components/dynamic/types"


export interface SemanticRendererProps<
  T = unknown
> {

  value: T

  onChange?: (value: T) => void

  readonly?: boolean

  context?: RenderContext

  platform?: Platform

  presentation?: PresentationNode
}

export type SemanticRenderer<
  T = unknown
> = FC<SemanticRendererProps<T>>