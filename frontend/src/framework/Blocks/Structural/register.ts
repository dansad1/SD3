// src/Blocks/Structural/index.ts


import { ContainerBlock } from "./ContainerBlock"
import { SectionBlock } from "./SectionBlock"
import { StackBlock } from "./StackBlock"
import { SplitBlock } from "./SplitBlock"
import { blockRegistry } from "../Registry/BlockRegistry"
import { PageActionsBlock } from "./Page_actionsBlock"

/* ========= RENDER ========= */

blockRegistry.register("container", ContainerBlock)
blockRegistry.register("section", SectionBlock)
blockRegistry.register("stack", StackBlock)
blockRegistry.register("split", SplitBlock)
blockRegistry.register("page_actions",PageActionsBlock)

export {}
