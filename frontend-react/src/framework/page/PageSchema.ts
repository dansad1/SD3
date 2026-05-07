import type { ActionBlock } from "../Blocks/Action/types";
import type { UploadBlock } from "../Blocks/Action/upload/types";
import type {
  BadgeBlock,
  DividerBlock,
  HeadingBlock,
  InsertVariablesBlock,
  SpacerBlock,
  TextBlock,
} from "../Blocks/Atom/types";
import type { ChatListBlock } from "../Blocks/ChatList/types";
import type { ChatThreadBlock } from "../Blocks/ChatThread/types";
import type { ForBlock, IfBlock } from "../Blocks/Control/types";
import type { ResourceBlock } from "../Blocks/Data/types";
import type { FormApiBlock } from "../Blocks/Form/types/api";
import type { MatrixApiBlock } from "../Blocks/Matrix/types/api";
import type { TabsBlock } from "../Blocks/Structural/Tabs/types";
import type {
  ContainerBlock,
  SectionBlock,
  SplitBlock,
  StackBlock,
} from "../Blocks/Structural/types";
import type { TableApiBlock } from "../Blocks/Table/types/api";
import type { CustomBlock } from "../Blocks/Content/Custom/types";

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
      | UploadBlock // ⭐ ВОТ НОВЫЙ
      | TableApiBlock
      | FormApiBlock
      | MatrixApiBlock
      | BadgeBlock
      | IfBlock
      | ForBlock
      | TabsBlock
      | ResourceBlock // ⭐ ВОТ ЭТО КЛЮЧЕВОЕ
      | InsertVariablesBlock
      | ChatThreadBlock
      | ChatListBlock | CustomBlock;
/*
 * Страница — просто контейнер блоков
 */
export interface ApiPageSchema {
  id: string;
  title?: string;
  blocks: ApiPageBlock[];
}

export type PageBlock = ApiPageBlock;
