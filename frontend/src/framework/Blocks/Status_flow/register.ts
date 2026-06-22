import { blockRegistry } from "@/framework/Blocks/Registry/BlockRegistry"
import { StatusFlowBlock } from "./Status_flowBlock"

export {}

blockRegistry.register("status_flow", StatusFlowBlock)
