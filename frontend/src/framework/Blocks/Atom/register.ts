// src/Blocks/Atom/index.ts


import { HeadingBlock } from "./HeadingBlock"
import { TextBlock } from "./TextBlock"
import { DividerBlock } from "./DividerBlock"
import { SpacerBlock } from "./SpacerBlock"
import { BadgeBlock } from "./BadgeBlock";
import { blockRegistry } from "../Registry/BlockRegistry";
import { InsertVariablesBlock } from "./InsertVariablesBlock/InsertVariablesBlock";
import { LinkBlock } from "./LinkBlock";

/* ========= RENDER ========= */

blockRegistry.register("heading", HeadingBlock)
blockRegistry.register("text", TextBlock)
blockRegistry.register("divider", DividerBlock)
blockRegistry.register("spacer", SpacerBlock)
blockRegistry.register("badge", BadgeBlock)
blockRegistry.register("insert_variables",InsertVariablesBlock)
blockRegistry.register("link", LinkBlock)

export {}