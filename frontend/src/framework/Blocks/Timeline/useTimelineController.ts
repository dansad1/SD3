import {
  useEffect,
  useMemo,
  useState,
} from "react"

import { APIClient } from "@/framework/api/client/APIClient"
import { resolveProps } from "@/framework/bind/expression/resolveProps"
import { usePageRuntimeContext } from "@/framework/page/runtime/usePageRuntimeContext"

import type { TimelineBlock } from "./types"


// =========================================================
// NORMALIZED VIEW MODEL
// =========================================================

export type TimelineChange = {
  before?: unknown
  after?: unknown

  label?: string
  fieldType?: string
}

export type TimelineActor = {
  id?: string | number
  label?: string
}

export type TimelineItem = {
  id: string | number

  action: string

  date?: string

  actor?: TimelineActor | null

  objectRepr?: string

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


// =========================================================
// RAW API TYPES
// =========================================================

type RawTimelineChange = {
  field?: string

  before?: unknown
  after?: unknown

  old_value?: unknown
  new_value?: unknown

  label?: string

  field_type?: string
  fieldType?: string
}

type RawTimelineItem = {
  id: string | number

  action: string

  date?: string
  created?: string

  actor?: TimelineActor | null

  object_repr?: string
  objectRepr?: string

  changes?:
    | Record<
        string,
        RawTimelineChange
      >
    | RawTimelineChange[]

  meta?: Record<
    string,
    unknown
  >
}

type TimelineResponse =
  | RawTimelineItem[]
  | {
      items?: RawTimelineItem[]
      rows?: RawTimelineItem[]
      results?: RawTimelineItem[]
    }


// =========================================================
// RESPONSE
// =========================================================

function normalizeResponse(
  response: TimelineResponse
): RawTimelineItem[] {
  if (Array.isArray(response)) {
    return response
  }

  return (
    response.items ??
    response.rows ??
    response.results ??
    []
  )
}


// =========================================================
// QUERY
// =========================================================

function buildQuery(
  params: Record<
    string,
    unknown
  >
): string {
  const query =
    new URLSearchParams()

  Object.entries(
    params
  ).forEach(
    ([key, value]) => {
      if (
        value === null ||
        value === undefined ||
        value === ""
      ) {
        return
      }

      if (
        typeof value === "object"
      ) {
        query.set(
          key,
          JSON.stringify(value)
        )

        return
      }

      query.set(
        key,
        String(value)
      )
    }
  )

  return query.toString()
}


// =========================================================
// CHANGE NORMALIZATION
// =========================================================

function normalizeChange(
  change: RawTimelineChange
): TimelineChange {
  return {
    before:
      change.before ??
      change.old_value,

    after:
      change.after ??
      change.new_value,

    label:
      change.label,

    fieldType:
      change.fieldType ??
      change.field_type,
  }
}

function normalizeChanges(
  changes: RawTimelineItem["changes"]
): Record<
  string,
  TimelineChange
> {
  if (!changes) {
    return {}
  }

  if (Array.isArray(changes)) {
    return changes.reduce<
      Record<
        string,
        TimelineChange
      >
    >(
      (
        result,
        change,
        index
      ) => {
        const field =
          change.field ||
          `change-${index}`

        result[field] =
          normalizeChange(
            change
          )

        return result
      },
      {}
    )
  }

  return Object.entries(
    changes
  ).reduce<
    Record<
      string,
      TimelineChange
    >
  >(
    (
      result,
      [field, change]
    ) => {
      result[field] =
        normalizeChange(
          change
        )

      return result
    },
    {}
  )
}


// =========================================================
// ITEM NORMALIZATION
// =========================================================

function normalizeItem(
  item: RawTimelineItem
): TimelineItem {
  return {
    id:
      item.id,

    action:
      item.action,

    date:
      item.date ??
      item.created,

    actor:
      item.actor ?? null,

    objectRepr:
      item.objectRepr ??
      item.object_repr,

    changes:
      normalizeChanges(
        item.changes
      ),

    meta:
      item.meta ?? {},
  }
}


// =========================================================
// CONTROLLER
// =========================================================

export function useTimelineController(
  block: TimelineBlock
): TimelineViewModel {
  const context =
    usePageRuntimeContext() as Record<
      string,
      unknown
    >

  const props = resolveProps(
    block as Record<
      string,
      unknown
    >,
    context
  ) as TimelineBlock & {
    items?: RawTimelineItem[]

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
    RawTimelineItem[]
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
          props.params ?? {}
        ),
      [props.params]
    )

 useEffect(() => {

  if (
    props.items ||
    !props.source
  ) {
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

      const url =
        queryString
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
    useMemo(
      () =>
        (
          props.items ??
          remoteItems
        ).map(
          normalizeItem
        ),
      [
        props.items,
        remoteItems,
      ]
    )

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

    reload: () => {
      setVersion(
        current =>
          current + 1
      )
    },
  }
}