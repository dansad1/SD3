import {
  semanticRendererRegistry
} from "@/framework/renderers/registry"
import { AttendanceCell } from "../renderers/matrix/AttendanceCell"
import type { SemanticRenderer } from "@/framework/renderers/types"



semanticRendererRegistry[
  "AttendanceCell"
] =
  AttendanceCell as SemanticRenderer<unknown>