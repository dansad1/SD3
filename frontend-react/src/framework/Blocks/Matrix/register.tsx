// src/Blocks/Matrix/index.ts


import { blockRegistry } from "../Registry/BlockRegistry"
import { MatrixDSLBlock } from "./MatrixDSL"

/* ========= RENDER ========= */

blockRegistry.register("matrix", MatrixDSLBlock)

export {}