import type { ActionBlock } from "../Blocks/Action/types";
import type { UploadBlock } from "../Blocks/Action/upload/types";
import type {
  BadgeBlock,
  DividerBlock,
  HeadingBlock,
  SpacerBlock,
  TextBlock,
} from "../Blocks/Atom/types";
import type { ChatListBlock } from "../Blocks/ChatList/types";
import type { ChatThreadBlock } from "../Blocks/ChatThread/types";
import type { ForBlock, IfBlock } from "../Blocks/Control/types";
import type { CustomBlock } from "../Blocks/Custom/types";
import type { ResourceBlock } from "../Blocks/Data/types";
import type { DocumentBlock } from "../Blocks/Document/types";
import type { FormApiBlock } from "../Blocks/Form/types/api";
import type { TabsBlock } from "../Blocks/Structural/Tabs/types";
import type {
  ContainerBlock,
  SectionBlock,
  SplitBlock,
  StackBlock,
} from "../Blocks/Structural/types";
import type { TableApiBlock } from "../Blocks/Table/types/api";

/**
 * Единый union всех декларативных блоков страницы
 */
export type ApiPageBlock =
  | ContainerBlock
  | StackBlock
  | SectionBlock
  | SplitBlock
  | HeadingBlock
  | TextBlock
  | DividerBlock
  | SpacerBlock
  | ActionBlock
  | UploadBlock
  | TableApiBlock
  | FormApiBlock
  | BadgeBlock
  | IfBlock
  | ForBlock
  | TabsBlock
  | ResourceBlock
  | ChatThreadBlock
  | ChatListBlock
  | CustomBlock
  | DocumentBlock


// =====================================================
// PAGE CHROME
// =====================================================

export interface PageChrome {

  mode?: "auth" | "app"

  footer?: boolean

  container?: boolean

  sidebar?: boolean

  navbar?: boolean

  fullscreen?: boolean

  centered?: boolean
}

// =====================================================
// PAGE SCHEMA
// =====================================================

export interface ApiPageSchema {

  id: string

  title?: string

  chrome?: PageChrome

  blocks: ApiPageBlock[]
}


export type PageBlock = ApiPageBlock