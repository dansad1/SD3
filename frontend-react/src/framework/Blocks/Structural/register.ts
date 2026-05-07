// src/Blocks/Structural/index.ts


import { ContainerBlock } from "./ContainerBlock"
import { SectionBlock } from "./SectionBlock"
import { StackBlock } from "./StackBlock"
import { SplitBlock } from "./SplitBlock"
import { blockRegistry } from "../Registry/BlockRegistry"

/* ========= RENDER ========= */

blockRegistry.register("container", ContainerBlock)
blockRegistry.register("section", SectionBlock)
blockRegistry.register("stack", StackBlock)
blockRegistry.register("split", SplitBlock)
export {}
