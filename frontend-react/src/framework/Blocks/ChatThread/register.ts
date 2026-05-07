import { blockRegistry } from "../Registry/BlockRegistry";
import { ChatThreadBlock } from "./ThreadBlock";

blockRegistry.register(
  "chat_thread",
  ChatThreadBlock
)
export {}