// src/framework/Blocks/Table/features/init.ts

import { registerTableFeature } from "./registry"

import { searchFeature } from "./search"
import { selectionFeature } from "./selection"
import { toolbarFeature } from "./toolbar"
import { visibleFieldsFeature } from "./visibleFieldsFeature"
import { rowActionsFeature } from "./rowActions"
import { rowClickFeature } from "./rowClick"
import { bulkActionsFeature } from "./bulkActions"

export function initTableFeatures() {
  registerTableFeature(searchFeature())
  registerTableFeature(selectionFeature())
  registerTableFeature(toolbarFeature())
  registerTableFeature(visibleFieldsFeature())
  registerTableFeature(rowClickFeature())
  registerTableFeature(rowActionsFeature())
  registerTableFeature(bulkActionsFeature())
}