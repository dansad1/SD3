/* eslint-disable @typescript-eslint/no-explicit-any */

import { useEffect, useState } from "react"


const NotificationOverview = () => {

  const [data, setData] = useState<any>(null)

  useEffect(() => {

    let active = true

    const load = async () => {

      const res = await fetch(

        "/api/resource/notification.overview/",

        {

          credentials: "include",

        }

      )

      if (!res.ok) {

        console.error(

          await res.text()

        )

        return

      }

      const json = await res.json()

      if (active) {

        setData(

          json

        )

      }

    }

    load()

    return () => {

      active = false

    }

  }, [])


  if (!data) {

    return (

      <div>

        Loading...

      </div>

    )

  }


  const renderTable = (

    title: string,

    rows: any[],

  ) => (

    <>

      <h3>

        {title}

      </h3>

      <div

        className="ui-table-wrapper"

      >

        <table

          className="ui-table"

        >

          <thead>

          <tr>

            <th>

              Роль

            </th>

            {

              data.events.map(

                (

                  event: any

                ) => (

                  <th

                    key={

                      event.code

                    }

                    title={

                      event.label

                    }

                  >

                    <div

                      className="th-content"

                    >

                      {

                        event.label

                      }

                    </div>

                  </th>

                )

              )

            }

            <th>

              Статусы

            </th>

          </tr>

          </thead>


          <tbody>

          {

            rows.length === 0

            ? (

              <tr>

                <td

                  className="empty"

                  colSpan={

                    data.events.length

                    +

                    2

                  }

                >

                  Нет данных

                </td>

              </tr>

            )

            : (

              rows.map(

                (

                  row: any

                ) => (

                  <tr

                    key={

                      row.id

                      ||

                      row.code

                    }

                  >

                    <td>

                      {

                        row.label

                      }

                    </td>


                    {

                      data.events.map(

                        (

                          event: any

                        ) => (

                          <td

                            key={

                              event.code

                            }

                          >

                            {

                              row.events.includes(

                                event.code

                              )

                              &&

                              "✔"

                            }

                          </td>

                        )

                      )

                    }


                    <td>

                      {

                        row.statuses.length

                        ?

                        row.statuses.join(

                          ", "

                        )

                        :

                        "—"

                      }

                    </td>

                  </tr>

                )

              )

            )

          }

          </tbody>

        </table>

      </div>

    </>

  )


  return (

    <>

      {

        renderTable(

          "Роли",

          data.roles,

        )

      }

      <br />

      {

        renderTable(

          "Логические роли",

          data.logical_roles,

        )

      }

    </>

  )

}


export default NotificationOverview