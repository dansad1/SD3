import { useMemo } from "react"


import type {
  WidgetProps,
  FieldSchema,
  Value,
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

export function PermissionEditorWidget(
  props: WidgetProps,
) {

  const {
    field,
    value,
    onChange,
    loading,
  } = props

  const groups =
    (
      field as PermissionFieldSchema
    ).groups ?? []

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

    const payload =
      Array.from(next)
        .map(String)

    onChange(
      payload as Value
    )
  }

  return (

    <BaseWidget
      field={field}
      loading={loading}
    >

      {({ disabled }) => (

        <div>

          {groups.map(
            group => (

              <div
                key={group.name}
                style={{
                  marginBottom: 24,
                }}
              >

                <div
                  style={{
                    fontWeight: 600,
                    marginBottom: 8,
                  }}
                >
                  {group.name}
                </div>

                <table className="table table-bordered">

                  <tbody>

                    {group.permissions.map(
                      permission => (

                        <tr
                          key={
                            permission.id
                          }
                        >

                          <td
                            style={{
                              width: 50,
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

                            <small
                              style={{
                                opacity: 0.65,
                              }}
                            >
                              {
                                permission.code
                              }
                            </small>

                            {permission.description && (

                              <div
                                style={{
                                  fontSize: 12,
                                  opacity: 0.7,
                                  marginTop: 2,
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

            )
          )}

        </div>

      )}

    </BaseWidget>

  )
}