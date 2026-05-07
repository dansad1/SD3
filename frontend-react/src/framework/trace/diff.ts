export function simpleDiff(
  before: unknown,
  after: unknown
) {
  try {

    const b = JSON.stringify(before, null, 2)
    const a = JSON.stringify(after, null, 2)

    if (b === a) {
      return {
        changed: false,
      }
    }

    return {
      changed: true,
      before,
      after,
    }

  } catch {
    return {
      changed: true,
      before: String(before),
      after: String(after),
    }
  }
}