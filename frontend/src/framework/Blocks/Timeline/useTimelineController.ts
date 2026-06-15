import { useEffect, useMemo, useState } from "react"

import { APIClient } from "@/framework/api/client/APIClient"
import { resolveProps } from "@/framework/bind/expression/resolveProps"
import { usePageRuntimeContext } from "@/framework/page/runtime/usePageRuntimeContext"

import type { TimelineBlock } from "./types"

export type TimelineChange = {
  before?: unknown
  after?: unknown

  old_value?: unknown
  new_value?: unknown

  label?: string
  field_type?: string
}

export type TimelineActor = {
  id?: string | number
  label?: string
}

export type TimelineItem = {
  id: string | number

  action: string

  date?: string
  created?: string

  actor?: TimelineActor | null

  object_repr?: string

  changes?: Record<
    string,
    TimelineChange
  >

  meta?: Record<
    string,
    unknown
  >
}

export type TimelineViewModel = {
  items: TimelineItem[]

  loading: boolean

  error: string | null

  emptyText: string

  compact: boolean

  reverse: boolean

  groupByDate: boolean

  reload: () => void
}

type TimelineResponse =
  | TimelineItem[]
  | {
      items?: TimelineItem[]
      rows?: TimelineItem[]
      results?: TimelineItem[]
    }

function normalizeResponse(
  response: TimelineResponse
): TimelineItem[] {
  if (Array.isArray(response)) {
    return response
  }

  return (
    response.items ||
    response.rows ||
    response.results ||
    []
  )
}

function buildQuery(
  params: Record<
    string,
    unknown
  >
) {
  const qs =
    new URLSearchParams()

  Object.entries(
    params || {}
  ).forEach(
    ([key, value]) => {
      if (
        value === null ||
        value === undefined ||
        value === ""
      ) {
        return
      }

      qs.set(
        key,
        String(value)
      )
    }
  )

  return qs.toString()
}

export function useTimelineController(
  block: TimelineBlock
): TimelineViewModel {

  const ctx =
    usePageRuntimeContext() as Record<
      string,
      unknown
    >

  const props = resolveProps(
    block as Record<
      string,
      unknown
    >,
    ctx
  ) as TimelineBlock & {
    items?: TimelineItem[]

    source?: string

    params?: Record<
      string,
      unknown
    >

    compact?: boolean

    reverse?: boolean

    groupByDate?: boolean

    emptyText?: string
  }

  const [
    remoteItems,
    setRemoteItems,
  ] = useState<
    TimelineItem[]
  >([])

  const [
    loading,
    setLoading,
  ] = useState(false)

  const [
    error,
    setError,
  ] = useState<
    string | null
  >(null)

  const [
    version,
    setVersion,
  ] = useState(0)

  const queryString =
    useMemo(
      () =>
        buildQuery(
          props.params || {}
        ),
      [props.params]
    )

  useEffect(() => {

    if (props.items) {
      return
    }

    if (!props.source) {
      return
    }

    let cancelled =
      false

    async function load() {

      setLoading(true)

      setError(null)

      try {

        const api =
          new APIClient()

       const url = queryString
  ? `/resource/${props.source}/?${queryString}`
  : `/resource/${props.source}/`
        const response =
          await api.get<TimelineResponse>(
            url
          )

        if (
          cancelled
        ) {
          return
        }

        setRemoteItems(
          normalizeResponse(
            response
          )
        )

      } catch (e) {

        if (
          cancelled
        ) {
          return
        }

        setError(
          e instanceof Error
            ? e.message
            : "Не удалось загрузить историю"
        )

      } finally {

        if (
          !cancelled
        ) {
          setLoading(
            false
          )
        }

      }

    }

    void load()

    return () => {
      cancelled =
        true
    }

  }, [
    props.items,
    props.source,
    queryString,
    version,
  ])

  const items =
    props.items ??
    remoteItems

  return {

    items,

    loading,

    error,

    emptyText:
      props.emptyText ||
      "История пока пуста",

    compact:
      Boolean(
        props.compact
      ),

    reverse:
      Boolean(
        props.reverse
      ),

    groupByDate:
      props.groupByDate !==
      false,

    reload: () =>
      setVersion(
        value =>
          value + 1
      ),
  }
}