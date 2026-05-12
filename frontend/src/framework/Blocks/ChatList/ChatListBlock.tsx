// src/framework/Blocks/Chat/ChatListBlock.tsx

import type { BlockComponent } from "../Registry/BlockRegistry"
import { ChatListEmpty } from "./ChatListEmpty"
import { ChatListSkeleton } from "./ChatListSkeleton"
import { ChatListView } from "./ChatListView"
import { useChatListData } from "./useChatListData"
import { useChatNavigation } from "./useChatNavigation"

export const ChatListBlock: BlockComponent<"chat_list"> = ({
  block,
}) => {
  const { items, selectedId } =
    useChatListData(block)

  const { openChat } =
    useChatNavigation()

  if (!Array.isArray(items)) {
    return <ChatListSkeleton />
  }

  if (items.length === 0) {
    return <ChatListEmpty />
  }

  return (
    <ChatListView
      items={items}
      selectedId={selectedId}
      onOpen={(id) => openChat(id, selectedId)}
      features={block.features}
    />
  )
}