// src/framework/normalize/normalizeDispatch.ts

import { normalizeAction } from "../Blocks/Action/normalize"

import {
  normalizeDivider,
  normalizeHeading,
  normalizeSpacer,
  normalizeText,
  normalizeBadge,
  normalizeInsertVariables,
} from "../Blocks/Atom/normalize"

import { normalizeForm } from "../Blocks/Form/Layout/normalize"
import { normalizeMatrix } from "../Blocks/Matrix/normalize"

import {
  normalizeContainer,
  normalizeSection,
  normalizeSplit,
  normalizeStack,
  
} from "../Blocks/Structural/normalize"

import { normalizeTable } from "../Blocks/Table/normalize"

import {
  normalizeIf,
  normalizeFor,
} from "../Blocks/Control/normalize"


import type {
  ApiPageBlock,
  PageBlock,
} from "../page/PageSchema"

import { normalizeResource } from "../Blocks/Data/runtime/normalize"
import { normalizeChatThread } from "../Blocks/ChatThread/normalize"
import { normalizeChatList } from "../Blocks/ChatList/normalize"
import { normalizeUpload } from "../Blocks/Action/upload/normalize"
import { normalizeTabs } from "../Blocks/Structural/Tabs/normalize"
import { normalizeCustom } from "../Blocks/Custom/normalize"

/**
 * Строго типизированная карта нормалайзеров.
 * Каждый type обязан вернуть тот же type.
 */
type BlockType = ApiPageBlock["type"]

type NormalizeMap = {
  [K in BlockType]: (
    block: Extract<ApiPageBlock, { type: K }>
  ) => Extract<PageBlock, { type: K }>
}

/**
 * Здесь регистрируются ВСЕ нормалайзеры.
 * Если добавишь новый блок — TS заставит добавить его сюда.
 */
export const normalizeMap: NormalizeMap = {
  table: normalizeTable,
  form: normalizeForm,
  matrix: normalizeMatrix,

  stack: normalizeStack,
  section: normalizeSection,
  split: normalizeSplit,
  container: normalizeContainer,
  tabs: normalizeTabs,

  heading: normalizeHeading,
  text: normalizeText,
  divider: normalizeDivider,
  spacer: normalizeSpacer,
  badge: normalizeBadge,
  insert_variables: normalizeInsertVariables,
chat_list: normalizeChatList,
  action: normalizeAction,
  upload: normalizeUpload,

  if: normalizeIf,
  for: normalizeFor,

  resource: normalizeResource,

  chat_thread: normalizeChatThread,
    custom: normalizeCustom
}

/**
 * Typed dispatch без bridge-cast.
 */
export function dispatchNormalize<
  T extends BlockType
>(
  block: Extract<ApiPageBlock, { type: T }>
): Extract<PageBlock, { type: T }> {
  const fn = normalizeMap[block.type]
  return fn(block)
}