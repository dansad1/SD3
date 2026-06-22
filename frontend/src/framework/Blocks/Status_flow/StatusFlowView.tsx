import type { StatusFlowVM } from "./types"


export function StatusFlowView({
  data,
  loading,
  error,
}: StatusFlowVM) {

  if (loading) {
    return <div>Загрузка...</div>
  }

  if (error) {
    return <div>{error}</div>
  }

  if (!data) {
    return null
  }

  const roles = Array.isArray(data.roles)
    ? data.roles
    : []

  const statuses = Array.isArray(data.statuses)
    ? data.statuses
    : []

  return (

    <div className="status-flow">

      {

        statuses.map(

          status => {

            const targets = Array.isArray(

              status.targets,

            )

              ? status.targets

              : []

            return (

              <div

                key={status.id}

                className="status-flow__card"

              >

                <div

                  className="status-flow__header"

                >

                  <span

                    className="status-flow__dot"

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

                  className="status-flow__table"

                >

                  <thead>

                    <tr>

                      <th />

                      {

                        roles.map(

                          role => (

                            <th

                              key={role.id}

                            >

                              {

                                role.name

                              }

                            </th>

                          )

                        )

                      }

                    </tr>

                  </thead>


                  <tbody>

                    {

                      targets.map(

                        target => {

                          const targetRoles =

                            Array.isArray(

                              target.roles,

                            )

                              ? target.roles

                              : []

                          return (

                            <tr

                              key={target.id}

                            >

                              <td>

                                {

                                  target.name

                                }

                              </td>


                              {

                                roles.map(

                                  role => (

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

                                          targetRoles.includes(

                                            role.name,

                                          )

                                        }

                                        readOnly

                                      />

                                    </td>

                                  )

                                )

                              }


                            </tr>

                          )

                        }

                      )
                    }
                  </tbody>
                </table>
              </div>
            )
          }
        )
      }
    </div>
  )
}