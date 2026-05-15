// src/framework/security/can.ts

import type { BlockCapabilities } from "../Blocks/BlockType"


/* =========================================================
   CAN
   ========================================================= */

/**
 * Runtime capability resolver.
 *
 * examples:
 *
 * can(block.capabilities, "edit")
 * can(block.capabilities, "run")
 * can(block.capabilities, "approve")
 */
export function can(
  capabilities: BlockCapabilities | undefined,
  action: string
): boolean {

  /**
   * no capabilities specified
   * = allowed
   */
  if (!capabilities) {
    return true
  }

  return capabilities[action] === true
}