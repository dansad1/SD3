import isEqual from "fast-deep-equal"

import type {
  FormRuntimeState,
  Reaction,
  RunPageEffect,
} from "./types"

import {
  applyAsyncEffects,
  applyLocalEffects,
} from "./applyEffects"

import {
  indexReactions,
  pickReactions,
} from "./indexReactions"

import {
  matchRule,
  shallowChangedFields,
} from "./utils"

type Params = {
  state: FormRuntimeState
  reactions?: Reaction[]
  changedFields: string[]
  runPageEffect?: RunPageEffect
  maxPasses?: number
}

async function processOnce(
  state: FormRuntimeState,
  reactions: Reaction[],
  runPageEffect?: RunPageEffect
): Promise<FormRuntimeState> {
  let next = state

  // sync
  for (const r of reactions) {
    if (!matchRule(r.match, next.values)) continue
    next = applyLocalEffects(next, r.effects, runPageEffect)
  }

  // async
  for (const r of reactions) {
    if (!matchRule(r.match, next.values)) continue
    next = await applyAsyncEffects(next, r.effects)
  }

  return next
}

export async function runReactions({
  state,
  reactions = [],
  changedFields,
  runPageEffect,
  maxPasses = 8,
}: Params): Promise<FormRuntimeState> {
  if (!reactions.length) return state
  if (!changedFields.length) return state

  const index = indexReactions(reactions)

  let current = state
  let queue = [...changedFields]

  for (let i = 0; i < maxPasses; i++) {
    const affected = pickReactions(index, queue)
    if (!affected.length) return current

    const next = await processOnce(
      current,
      affected,
      runPageEffect
    )

    if (isEqual(next, current)) return next

    const changed = shallowChangedFields(
      current.values,
      next.values
    )

    if (!changed.length) return next

    queue = changed
    current = next
  }

  console.warn("Reaction cycle detected", { changedFields })
  return current
}