// src/Blocks/Table/index.ts

import { blockRegistry } from "../Registry/BlockRegistry"
import { TableDSLBlock } from "./TableDSL"

/* ========= RENDER ========= */

blockRegistry.register("table", TableDSLBlock)

export {}