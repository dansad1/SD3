import {
  useCallback,
  useMemo,
  useState,
} from "react"

import {
  APIClient,
} from "@/framework/api/client/APIClient"

import {
  useResourceDataSource,
} from "../Data/sources/useResourceDataSource"

import type {
  Role,
  StatusFlowChange,
  StatusFlowData,
} from "./types"


const apiClient = new APIClient()


type SaveResponse = {
  status: "ok" | "error"

  updated?: number

  errors?: Record<
    string,
    string[]
  >
}


function buildChangeKey(
  sourceStatusId: number,
  targetStatusId: number,
  roleId: number,
): string {
  return [
    sourceStatusId,
    targetStatusId,
    roleId,
  ].join(":")
}


function getErrorMessage(
  error: unknown,
): string | null {
  if (!error) {
    return null
  }

  if (error instanceof Error) {
    return error.message
  }

  if (typeof error === "string") {
    return error
  }

  if (
    typeof error === "object"
    && error !== null
    && "message" in error
  ) {
    const message = (
      error as {
        message?: unknown
      }
    ).message

    if (typeof message === "string") {
      return message
    }
  }

  return "Произошла ошибка"
}


function getInitialEnabled(
  data: StatusFlowData | null,
  sourceStatusId: number,
  targetStatusId: number,
  roleId: number,
): boolean {
  const sourceStatus =
    data?.statuses.find(
      (status) => (
        status.id
        === sourceStatusId
      ),
    )

  const target =
    sourceStatus?.targets.find(
      (item) => (
        item.id
        === targetStatusId
      ),
    )

  const roleIds =
    Array.isArray(
      target?.roleIds,
    )
      ? target.roleIds
      : []

  return roleIds.includes(
    roleId,
  )
}


function applyChanges(
  sourceData: StatusFlowData | null,
  changes: Record<
    string,
    StatusFlowChange
  >,
): StatusFlowData | null {
  if (!sourceData) {
    return null
  }

  const roles =
    Array.isArray(
      sourceData.roles,
    )
      ? sourceData.roles
      : []

  const statuses =
    Array.isArray(
      sourceData.statuses,
    )
      ? sourceData.statuses
      : []

  const changeMap = new Map<
    string,
    boolean
  >()

  for (
    const change
    of Object.values(changes)
  ) {
    const key =
      buildChangeKey(
        change.sourceId,
        change.targetId,
        change.roleId,
      )

    changeMap.set(
      key,
      change.enabled,
    )
  }

  return {
    roles: roles.map(
      (role) => ({
        ...role,
      }),
    ),

    statuses: statuses.map(
      (status) => {
        const targets =
          Array.isArray(
            status.targets,
          )
            ? status.targets
            : []

        return {
          ...status,

          targets: targets.map(
            (target) => {
              const currentRoleIds =
                new Set<number>(
                  Array.isArray(
                    target.roleIds,
                  )
                    ? target.roleIds
                    : [],
                )

              for (
                const role
                of roles
              ) {
                const key =
                  buildChangeKey(
                    status.id,
                    target.id,
                    role.id,
                  )

                const enabled =
                  changeMap.get(
                    key,
                  )

                if (
                  enabled
                  === undefined
                ) {
                  continue
                }

                if (enabled) {
                  currentRoleIds.add(
                    role.id,
                  )
                } else {
                  currentRoleIds.delete(
                    role.id,
                  )
                }
              }

              return {
                ...target,

                roleIds:
                  Array.from(
                    currentRoleIds,
                  ),
              }
            },
          ),
        }
      },
    ),
  }
}


export function useStatusFlow(
  source: string,
  editable: boolean,
) {
  const resource =
    useResourceDataSource<StatusFlowData>({
      data: `resource:${source}`,
    })

  const [
    changes,
    setChanges,
  ] = useState<
    Record<
      string,
      StatusFlowChange
    >
  >({})

  const [
    saving,
    setSaving,
  ] = useState(false)

  const [
    saveError,
    setSaveError,
  ] = useState<
    string | null
  >(null)

  const sourceData =
    useMemo<
      StatusFlowData | null
    >(
      () => {
        const rawData =
          resource.data

        if (!rawData) {
          return null
        }

        return {
          roles:
            Array.isArray(
              rawData.roles,
            )
              ? rawData.roles
              : [],

          statuses:
            Array.isArray(
              rawData.statuses,
            )
              ? rawData.statuses
              : [],
        }
      },
      [resource.data],
    )

  const data =
    useMemo(
      () => (
        applyChanges(
          sourceData,
          changes,
        )
      ),
      [
        sourceData,
        changes,
      ],
    )

  const dirty =
    Object.keys(
      changes,
    ).length > 0

  const toggleRole =
    useCallback(
      (
        sourceStatusId: number,
        targetStatusId: number,
        role: Role,
        enabled: boolean,
      ) => {
        if (!editable) {
          return
        }

        const key =
          buildChangeKey(
            sourceStatusId,
            targetStatusId,
            role.id,
          )

        const initiallyEnabled =
          getInitialEnabled(
            sourceData,
            sourceStatusId,
            targetStatusId,
            role.id,
          )

        setChanges(
          (previous) => {
            if (
              enabled
              === initiallyEnabled
            ) {
              const next = {
                ...previous,
              }

              delete next[key]

              return next
            }

            return {
              ...previous,

              [key]: {
                sourceId:
                  sourceStatusId,

                targetId:
                  targetStatusId,

                roleId:
                  role.id,

                enabled,
              },
            }
          },
        )

        setSaveError(
          null,
        )
      },
      [
        editable,
        sourceData,
      ],
    )

  const submit =
    useCallback(
      async () => {
        const pendingChanges =
          Object.values(
            changes,
          )

        if (
          saving
          || pendingChanges.length === 0
        ) {
          return
        }

        setSaving(
          true,
        )

        setSaveError(
          null,
        )

        try {
          const response =
            await apiClient.post<
              SaveResponse,
              {
                changes:
                  StatusFlowChange[]
              }
            >(
              "/action/"
              + "ticket.workflow.save/"
              + "submit/",
              {
                changes:
                  pendingChanges,
              },
            )

          if (
            response.status
            !== "ok"
          ) {
            const backendError =
              response.errors
                ? Object.values(
                    response.errors,
                  )
                  .flat()
                  .join(" ")
                : null

            throw new Error(
              backendError
              || "Не удалось сохранить переходы.",
            )
          }

          setChanges(
            {},
          )
        } catch (error) {
          const message =
            getErrorMessage(
              error,
            )
            ?? "Ошибка сохранения"

          setSaveError(
            message,
          )

          throw error
        } finally {
          setSaving(
            false,
          )
        }
      },
      [
        changes,
        saving,
      ],
    )

  const reload =
    useCallback(
      () => {
        setChanges(
          {},
        )

        setSaveError(
          null,
        )
      },
      [],
    )

  return {
    data,

    loading:
      resource.loading,

    saving,

    dirty,
    editable,

    error:
      saveError
      ?? getErrorMessage(
        resource.error,
      ),

    toggleRole,

    submit,

    reload,
  }
}