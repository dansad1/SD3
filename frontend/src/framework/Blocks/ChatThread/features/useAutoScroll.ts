import { useEffect, useRef } from "react"

export function useAutoScroll(
  enabled: boolean | undefined,
  ref: React.RefObject<HTMLDivElement | null>,
  dep: number
) {
  const isUserNearBottom = useRef(true)

  useEffect(() => {
    const el = ref.current
    if (!el) return

    const handleScroll = () => {
      const threshold = 120

      const atBottom =
        el.scrollHeight - el.scrollTop - el.clientHeight < threshold

      isUserNearBottom.current = atBottom
    }

    el.addEventListener("scroll", handleScroll)

    return () => {
      el.removeEventListener("scroll", handleScroll)
    }
  }, [ref])

  useEffect(() => {
    const el = ref.current
    if (!el || !enabled) return

    if (isUserNearBottom.current) {
      el.scrollTo({
        top: el.scrollHeight,
        behavior: "smooth",
      })
    }
  }, [dep, enabled, ref])
}