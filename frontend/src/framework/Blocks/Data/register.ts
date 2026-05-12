// Blocks/Data/index.ts

import { blockRegistry } from "../Registry/BlockRegistry"
import { ResourceBlockComponent } from "./render/ResourceBlock"

blockRegistry.register("resource", ResourceBlockComponent)