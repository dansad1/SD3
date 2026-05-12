// src/Blocks/Control/index.ts

import { blockRegistry } from "../Registry/BlockRegistry"
import { ForBlock } from "./ForBlock"
import { IfBlock } from "./IfBlock"

/* ========= RENDER ========= */

blockRegistry.register("if", IfBlock)
blockRegistry.register("for", ForBlock)

export {}