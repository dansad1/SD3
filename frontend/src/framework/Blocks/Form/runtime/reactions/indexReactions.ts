import type { Reaction } from "./types"

export type ReactionIndex = Map<string, Reaction[]>

export function indexReactions(
  reactions: Reaction[] = []
): ReactionIndex {
  const index: ReactionIndex = new Map()

  for (const reaction of reactions) {
    for (const field of reaction.watch) {
      const list = index.get(field) ?? []
      list.push(reaction)
      index.set(field, list)
    }
  }

  return index
}

export function pickReactions(
  index: ReactionIndex,
  changedFields: string[]
): Reaction[] {
  const result = new Map<string, Reaction>()

  for (const field of changedFields) {
    const list = index.get(field) ?? []

    for (const reaction of list) {
      result.set(
        reaction.id ?? JSON.stringify(reaction),
        reaction
      )
    }
  }

  return Array.from(result.values())
}