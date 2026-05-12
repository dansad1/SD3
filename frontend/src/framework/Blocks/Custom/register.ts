import { blockRegistry } from "@/framework/Blocks/Registry/BlockRegistry"
import { CustomBlock } from "./CustomBlock"

export {}

blockRegistry.register("custom", CustomBlock)
