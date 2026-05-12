// form/hooks/submit/resolveRedirectTarget.ts

type RedirectTarget =
  | string
  | {
      to: string
      ctx?: Record<string, unknown>
    }

export function resolveRedirectTarget(
  redirect?: RedirectTarget,
  backendRedirect?: unknown
): RedirectTarget | undefined {
  return (
    redirect ||
    (backendRedirect as RedirectTarget | undefined)
  )
}