import {
  useMemo,
  useState,
} from "react"

import type {
  WidgetProps,
  FieldSchema,
} from "../types"

import { BaseWidget } from "./Base"

type PermissionOption = {
  id: number
  value: number
  code: string
  label: string
  description?: string
}

type PermissionGroup = {
  name: string
  permissions: PermissionOption[]
}

type PermissionFieldSchema =
  FieldSchema & {
    groups?: PermissionGroup[]
  }

type PermissionValue = {
  value: number | string
  label?: string
}

function isPermissionValue(
  item: unknown,
): item is PermissionValue {

  return (
    typeof item === "object"
    && item !== null
    && "value" in item
  )

}

function getPermissionGroupName(
  code: string,
): string {

  const normalizedCode =
    String(
      code ?? ""
    ).trim()

  if (
    !normalizedCode
  ) {
    return "Общее"
  }

  const separatorIndex =
    normalizedCode.indexOf(
      "."
    )

  if (
    separatorIndex <= 0
  ) {
    return "Общее"
  }

  return normalizedCode.slice(
    0,
    separatorIndex
  )

}

export function PermissionEditorWidget(
  props: WidgetProps,
) {

  const {
    field,
    value,
    onChange,
    loading,
  } = props

  const groups = useMemo(
    () => {

      const sourceGroups =
        (
          field as PermissionFieldSchema
        ).groups ?? []

      const permissions =
        sourceGroups.flatMap(
          group =>
            group.permissions
        )

      const grouped =
        new Map<
          string,
          PermissionOption[]
        >()

      for (
        const permission
        of permissions
      ) {

        const groupName =
          getPermissionGroupName(
            permission.code
          )

        const groupPermissions =
          grouped.get(
            groupName
          ) ?? []

        groupPermissions.push(
          permission
        )

        grouped.set(
          groupName,
          groupPermissions
        )

      }

      return Array
        .from(
          grouped.entries()
        )
        .map(
          (
            [
              name,
              groupPermissions,
            ]
          ) => ({
            name,
            permissions:
              groupPermissions.sort(
                (
                  first,
                  second,
                ) =>
                  first.code.localeCompare(
                    second.code
                  )
              ),
          })
        )
        .sort(
          (
            first,
            second,
          ) =>
            first.name.localeCompare(
              second.name
            )
        )

    },
    [field]
  )

  const [activeTab, setActiveTab] =
    useState<string | null>(
      null
    )

  const currentTab =
    activeTab
    ?? groups[0]?.name
    ?? ""

  const currentGroup =
    groups.find(
      group =>
        group.name === currentTab
    )
    ?? groups[0]

  const selected = useMemo(
    () => {

      const result =
        new Set<number>()

      if (
        !Array.isArray(value)
      ) {
        return result
      }

      for (const item of value) {

        if (
          isPermissionValue(item)
        ) {

          const id =
            Number(item.value)

          if (
            Number.isFinite(id)
          ) {

            result.add(id)

          }

          continue

        }

        const id =
          Number(item)

        if (
          Number.isFinite(id)
        ) {

          result.add(id)

        }

      }

      return result

    },
    [value]
  )

  function updateSelection(
    ids: Set<number>,
  ) {

    onChange(
      Array
        .from(ids)
        .map(String)
    )

  }

  function toggle(
    permissionId: number,
  ) {

    const next =
      new Set(selected)

    if (
      next.has(
        permissionId
      )
    ) {

      next.delete(
        permissionId
      )

    } else {

      next.add(
        permissionId
      )

    }

    updateSelection(
      next
    )

  }

  function selectAllCurrent() {

    if (
      !currentGroup
    ) {
      return
    }

    const next =
      new Set(selected)

    for (
      const permission
      of currentGroup.permissions
    ) {

      next.add(
        permission.id
      )

    }

    updateSelection(
      next
    )

  }

  function clearCurrent() {

    if (
      !currentGroup
    ) {
      return
    }

    const next =
      new Set(selected)

    for (
      const permission
      of currentGroup.permissions
    ) {

      next.delete(
        permission.id
      )

    }

    updateSelection(
      next
    )

  }

  return (

    <BaseWidget
      field={field}
      loading={loading}
    >

      {({ disabled }) => (

        <div className="ui-tabs ui-tabs-line">

          <div className="ui-tabs-header">

            {groups.map(
              group => {

                const count =
                  group.permissions.filter(
                    permission =>
                      selected.has(
                        permission.id
                      )
                  ).length

                return (

                  <button
                    key={group.name}
                    type="button"
                    disabled={disabled}
                    className={
                      group.name === currentTab
                        ? "ui-tab active"
                        : "ui-tab"
                    }
                    onClick={() =>
                      setActiveTab(
                        group.name
                      )
                    }
                  >

                    {group.name}

                    {count > 0 && (
                      <>
                        {" "}
                        (
                        {count}
                        )
                      </>
                    )}

                  </button>

                )

              }
            )}

          </div>

          <div className="ui-tabs-body">

            <div
              style={{
                display: "flex",
                gap: 8,
                marginBottom: 12,
              }}
            >

              <button
                type="button"
                className="ui-btn"
                disabled={disabled}
                onClick={
                  selectAllCurrent
                }
              >
                Выбрать всё
              </button>

              <button
                type="button"
                className="ui-btn"
                disabled={disabled}
                onClick={
                  clearCurrent
                }
              >
                Снять всё
              </button>

            </div>

            <div className="ui-table-wrapper">

              <table className="ui-table">

                <thead>

                  <tr>

                    <th
                      style={{
                        width: 60,
                        textAlign:
                          "center",
                      }}
                    >
                      ✓
                    </th>

                    <th>
                      Право
                    </th>

                  </tr>

                </thead>

                <tbody>

                  {currentGroup?.permissions.map(
                    permission => (

                      <tr
                        key={
                          permission.id
                        }
                      >

                        <td
                          style={{
                            textAlign:
                              "center",
                          }}
                        >

                          <input
                            type="checkbox"
                            disabled={
                              disabled
                            }
                            checked={
                              selected.has(
                                permission.id
                              )
                            }
                            onChange={() =>
                              toggle(
                                permission.id
                              )
                            }
                          />

                        </td>

                        <td>

                          <div>
                            {
                              permission.label
                            }
                          </div>

                          <div
                            style={{
                              fontSize: 12,
                              opacity: 0.7,
                            }}
                          >
                            {
                              permission.code
                            }
                          </div>

                          {permission.description && (

                            <div
                              style={{
                                fontSize: 12,
                                opacity: 0.7,
                                marginTop: 4,
                              }}
                            >
                              {
                                permission.description
                              }
                            </div>

                          )}

                        </td>

                      </tr>

                    )
                  )}

                </tbody>

              </table>

            </div>

          </div>

        </div>

      )}

    </BaseWidget>

  )

}