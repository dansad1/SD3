import { useEffect, useRef } from "react"
import type { Json } from "@/framework/types/json"

type FormValues = Record<string, Json>

type Params = {
  entity?: string
  objectId?: string | number | null
  initial?: FormValues | null
  mode?: "create" | "edit" | "view"

  form: {
    setInitialValues: (values: FormValues) => void
  }
}

export function useFormInitialData({
  entity,
  objectId,
  initial,
  mode,
  form,
}: Params) {
  const initializedRef = useRef<string | null>(null)

  useEffect(() => {
    initializedRef.current = null
  }, [entity, objectId])

  useEffect(() => {
    const key = `${entity}:${objectId ?? "create"}`

    const mergedData =
      initial && Object.keys(initial).length > 0
        ? initial
        : {}

    const mergedKey = JSON.stringify(mergedData)

    if (initializedRef.current === `${key}:${mergedKey}`) {
      return
    }

    if (Object.keys(mergedData).length === 0) {
      return
    }

    form.setInitialValues(mergedData)

    initializedRef.current = `${key}:${mergedKey}`

    console.log("🟢 FORM INITIALIZED", {
      key,
      mode,
      initial,
      mergedData,
    })
  }, [entity, objectId, mode, initial, form])
}