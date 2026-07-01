/* eslint-disable @typescript-eslint/no-explicit-any */

import { useEffect, useState } from "react"

import { MatrixBlock } from "@/framework/Blocks/Matrix/MatrixBlock"
import Modal from "@/framework/components/ui/Modal"

type SelectedRecipient = {
  recipient: string
  label: string
}

const NotificationOverview = () => {

  const [data, setData] = useState<any>(null)

  const [
    selected,
    setSelected,
  ] = useState<SelectedRecipient | null>(
    null,
  )

  useEffect(() => {

    let active = true

    const load = async () => {

      const res = await fetch(

        "/api/resource/notification.overview/",

        {
          credentials: "include",
        },

      )

      if (!res.ok) {

        console.error(
          await res.text(),
        )

        return

      }

      const json = await res.json()

      if (active) {

        setData(
          json,
        )

      }

    }

    void load()

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

    logical = false,

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
                    event: any,
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

                        {event.label}

                      </div>

                    </th>

                  ),

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
                      row: any,
                    ) => {

                      const recipient = logical

                        ? `logical:${row.code}`

                        : `role:${row.id}`

                      return (

                        <tr

                          key={
                            row.id
                            ||
                            row.code
                          }

                          style={{
                            cursor:
                              "pointer",
                          }}

                          onClick={() =>

                            setSelected({

                              recipient,

                              label:
                                row.label,

                            })

                          }

                        >

                          <td>

                            {row.label}

                          </td>

                          {

                            data.events.map(

                              (
                                event: any,
                              ) => (

                                <td
                                  key={
                                    event.code
                                  }
                                >

                                  {

                                    row.events.includes(

                                      event.code,

                                    )

                                      ? "✔"

                                      : ""

                                  }

                                </td>

                              ),

                            )

                          }

                          <td>

                            {

                              row.statuses.length

                                ? row.statuses.join(

                                    ", ",

                                  )

                                : "—"

                            }

                          </td>

                        </tr>

                      )

                    },

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

          true,

        )

      }

      <Modal

        isOpen={
          selected !== null
        }

        onClose={() =>

          setSelected(
            null,
          )

        }

        title={
          selected
            ? `Уведомления — ${selected.label}`
            : ""
        }

        width="95vw"

      >

        {

          selected && (

            <div
              style={{
                display: "flex",
                flexDirection: "column",
                gap: 24,
              }}
            >

              <div>

                <h3>

                  События

                </h3>

                <MatrixBlock

                  block={{

                    code:
                      "notification-recipient",

                    params: {

                      recipient:
                        selected.recipient,

                    },

                  }}

                />

              </div>

              <div>

                <h3>

                  Статусы

                </h3>

                <MatrixBlock

                  block={{

                    code:
                      "notification-status",

                    params: {

                      recipient:
                        selected.recipient,

                    },

                  }}

                />

              </div>

            </div>

          )

        }

      </Modal>

    </>

  )

}

export default NotificationOverview