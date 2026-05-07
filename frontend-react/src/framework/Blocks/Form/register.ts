import { blockRegistry } from "../Registry/BlockRegistry"
import { FormDslBlock } from "./Block/FormDSLBlock"

blockRegistry.register("form", FormDslBlock)

export {}