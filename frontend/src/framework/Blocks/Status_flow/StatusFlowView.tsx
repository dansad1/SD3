import type { StatusFlowVM } from "./types"



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
      <section className="ui-section">
        <div className="ui-matrix-loading">
          Загрузка переходов...
        </div>
      </section>
    )
  }

  if (!data) {
    return (
      <section className="ui-section">
        <div className="ui-matrix-empty">
          Данные схемы переходов не получены
        </div>
      </section>
    )
  }

  const roles = Array.isArray(data.roles)
    ? data.roles
    : []

  const statuses = Array.isArray(data.statuses)
    ? data.statuses
    : []

  const controlsDisabled = saving || !editable

  return (
    <section
      className="ui-section"
      aria-label="Матрица переходов статусов"
      aria-busy={saving}
    >
      <header className="ui-section-header status-flow__header">
        <div>
          <h2 className="ui-section-title">
            Переходы статусов
          </h2>

          <p className="status-flow__description">
            Укажите роли, которым разрешён переход
            в следующий статус.
          </p>
        </div>

        {dirty && (
          <span
            className="status-flow__dirty"
            role="status"
          >
            Есть несохранённые изменения
          </span>
        )}
      </header>

      <div className="ui-section-body">
        {error && (
          <div
            className="status-flow__error"
            role="alert"
          >
            {error}
          </div>
        )}

        {statuses.length === 0 ? (
          <div className="ui-matrix-empty">
            Переходы статусов пока не настроены
          </div>
        ) : (
          <div className="status-flow">
            {statuses.map((status) => {
              const targets = Array.isArray(status.targets)
                ? status.targets
                : []

              return (
                <section
                  key={status.id}
                  className="status-flow__item"
                >
                  <header className="status-flow__item-header">
                    <span
                      className="status-flow__dot"
                      style={{
                        backgroundColor:
                          status.color || "var(--text-soft)",
                      }}
                      aria-hidden="true"
                    />

                    <strong>{status.name}</strong>
                  </header>

                  {targets.length === 0 ? (
                    <div className="ui-matrix-empty">
                      Нет доступных переходов
                    </div>
                  ) : (
                    <div className="ui-matrix-wrapper">
                      <div className="ui-matrix">
                        <table className="ui-matrix-table">
                          <thead>
                            <tr>
                              <th
                                className={
                                  "ui-matrix-sticky-top "
                                  + "ui-matrix-sticky-left"
                                }
                                scope="col"
                              >
                                Следующий статус
                              </th>

                              {roles.map((role) => (
                                <th
                                  key={role.id}
                                  className="ui-matrix-sticky-top"
                                  scope="col"
                                >
                                  {role.name}
                                </th>
                              ))}
                            </tr>
                          </thead>

                          <tbody>
                            {targets.map((target) => {
                              const roleIds = Array.isArray(
                                target.roleIds,
                              )
                                ? target.roleIds
                                : []

                              return (
                                <tr key={target.id}>
                                  <th
                                    className="ui-matrix-sticky-left"
                                    scope="row"
                                  >
                                    {target.name}
                                  </th>

                                  {roles.map((role) => {
                                    const inputId = [
                                      "status-flow",
                                      status.id,
                                      target.id,
                                      role.id,
                                    ].join("-")

                                    return (
                                      <td key={role.id}>
                                        <label
                                          className="ui-checkbox-item status-flow__checkbox"
                                          htmlFor={inputId}
                                        >
                                          <input
                                            id={inputId}
                                            type="checkbox"
                                            checked={roleIds.includes(
                                              role.id,
                                            )}
                                            disabled={controlsDisabled}
                                            aria-label={
                                              `${role.name}: `
                                              + `${status.name} → `
                                              + target.name
                                            }
                                            onChange={(event) => {
                                              toggleRole(
                                                status.id,
                                                target.id,
                                                role,
                                                event.currentTarget.checked,
                                              )
                                            }}
                                          />
                                        </label>
                                      </td>
                                    )
                                  })}
                                </tr>
                              )
                            })}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )}
                </section>
              )
            })}
          </div>
        )}

        {editable && (
          <footer className="status-flow__actions">
            <span className="status-flow__save-state">
              {saving
                ? "Сохранение..."
                : dirty
                  ? "Изменения не сохранены"
                  : "Изменения сохранены"}
            </span>

            <div className="status-flow__buttons">
              <button
                type="button"
                className="ui-btn ui-btn-secondary ui-btn-sm"
                disabled={!dirty || saving}
                onClick={reload}
              >
                Отменить
              </button>

              <button
                type="button"
                className={
                  "ui-btn ui-btn-primary ui-btn-sm"
                  + (saving ? " is-loading" : "")
                }
                disabled={!dirty || saving}
                onClick={() => {
                  void submit()
                }}
              >
                Сохранить
              </button>
            </div>
          </footer>
        )}
      </div>
    </section>
  )
}