import type {
  StatusFlowVM,
} from "./types"


export function StatusFlowView({
  data,
  loading,
  saving,
  dirty,
  editable,
  error,
  toggleRole,
  submit,
  reload,
}: StatusFlowVM) {
  if (loading) {
    return (
      <div>
        Загрузка...
      </div>
    )
  }

  if (!data) {
    return null
  }

  const roles =
    Array.isArray(
      data.roles,
    )
      ? data.roles
      : []

  const statuses =
    Array.isArray(
      data.statuses,
    )
      ? data.statuses
      : []

  return (
    <div className="status-flow">
      {statuses.map(
        (status) => {
          const targets =
            Array.isArray(
              status.targets,
            )
              ? status.targets
              : []

          return (
            <div
              key={status.id}
              className={
                "status-flow__card"
              }
            >
              <div
                className={
                  "status-flow__header"
                }
              >
                <span
                  className={
                    "status-flow__dot"
                  }
                  style={{
                    background:
                      status.color,
                  }}
                />

                <strong>
                  {status.name}
                </strong>
              </div>

              <table
                className={
                  "status-flow__table"
                }
              >
                <thead>
                  <tr>
                    <th />

                    {roles.map(
                      (role) => (
                        <th
                          key={role.id}
                        >
                          {role.name}
                        </th>
                      ),
                    )}
                  </tr>
                </thead>

                <tbody>
                  {targets.map(
                    (target) => {
                      const targetRoleIds =
                        Array.isArray(
                          target.roleIds,
                        )
                          ? target.roleIds
                          : []

                      return (
                        <tr
                          key={
                            target.id
                          }
                        >
                          <td>
                            {target.name}
                          </td>

                          {roles.map(
                            (role) => {
                              const checked =
                                targetRoleIds
                                  .includes(
                                    role.id,
                                  )

                              return (
                                <td
                                  key={
                                    role.id
                                  }
                                  className={
                                    "status-flow__checkbox"
                                  }
                                >
                                  <input
                                    type="checkbox"
                                    checked={
                                      checked
                                    }
                                    disabled={
                                      !editable
                                      || saving
                                    }
                                    onChange={(
                                      event,
                                    ) => {
                                      toggleRole(
                                        status.id,
                                        target.id,
                                        role,
                                        event
                                          .target
                                          .checked,
                                      )
                                    }}
                                  />
                                </td>
                              )
                            },
                          )}
                        </tr>
                      )
                    },
                  )}
                </tbody>
              </table>
            </div>
          )
        },
      )}

      {editable && (
        <div
          className={
            "status-flow__actions"
          }
        >
          <button
            type="button"
            disabled={
              !dirty
              || saving
            }
            onClick={() => {
              void submit()
            }}
          >
            {saving
              ? "Сохранение..."
              : "Сохранить"}
          </button>

          <button
            type="button"
            disabled={
              !dirty
              || saving
            }
            onClick={reload}
          >
            Отменить
          </button>
        </div>
      )}

      {error && (
        <div
          role="alert"
          className={
            "status-flow__error"
          }
        >
          {error}
        </div>
      )}
    </div>
  )
}