/* eslint-disable @typescript-eslint/no-explicit-any */

import { navigateAction } from "@/framework/Blocks/Action/handlers/navigateAction"
import { useEffect, useMemo, useState } from "react"


type TicketType = {
  id: number
  title: string
  description?: string
  service: number
  type: number
}

type Service = {
  id: number
  title: string
  description?: string
  types: TicketType[]
}

const TicketTypeSelect = () => {

  const [data, setData] = useState<any>(null)

  const [
    selected,
    setSelected,
  ] = useState<Service | null>(
    null,
  )

  const [
    search,
    setSearch,
  ] = useState("")

  useEffect(() => {

    let active = true

    const load = async () => {

      const res = await fetch(

        "/api/resource/ticket.create.select/",

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

      if (!active) {

        return

      }

      setData(
        json,
      )

      if (
        json.services.length
      ) {

        setSelected(
          json.services[0],
        )

      }

    }

    void load()

    return () => {

      active = false

    }

  }, [])

  const services = useMemo(() => {

    if (!data) {

      return []

    }

    if (!search) {

      return data.services

    }

    const value = search.toLowerCase()

    return data.services.filter(

      (service: Service) =>

        service.title
          .toLowerCase()
          .includes(value)

        ||

        service.description
          ?.toLowerCase()
          .includes(value),

    )

  }, [

    data,

    search,

  ])

  if (!data) {

    return (

      <div>

        Loading...

      </div>

    )

  }

  return (

    <div

      style={{

        display: "grid",

        gridTemplateColumns: "320px 1fr",

        border: "1px solid #e5e7eb",

        borderRadius: 14,

        overflow: "hidden",

        background: "#fff",

        minHeight: 650,

      }}

    >

      {/* ================================================= */}
      {/* SIDEBAR */}
      {/* ================================================= */}

      <div

        style={{

          display: "flex",

          flexDirection: "column",

          borderRight: "1px solid #eee",

        }}

      >

        <div

          style={{

            padding: 16,

            borderBottom: "1px solid #eee",

          }}

        >

          <input

            value={search}

            onChange={e =>

              setSearch(
                e.target.value,
              )

            }

            placeholder="Поиск сервиса..."

            style={{

              width: "100%",

              padding: "10px 12px",

              border: "1px solid #ddd",

              borderRadius: 8,

              fontSize: 14,

              outline: "none",

            }}

          />

        </div>

        <div

          style={{

            flex: 1,

            overflow: "auto",

          }}

        >

          {

            services.map(

              service => (

                <div

                  key={service.id}

                  onClick={() =>

                    setSelected(
                      service,
                    )

                  }

                  style={{

                    cursor: "pointer",

                    padding: 18,

                    transition: ".15s",

                    borderLeft:

                      selected?.id === service.id

                        ? "4px solid #2563eb"

                        : "4px solid transparent",

                    background:

                      selected?.id === service.id

                        ? "#eff6ff"

                        : "#fff",

                  }}

                >

                  <div

                    style={{

                      fontWeight: 600,

                    }}

                  >

                    {service.title}

                  </div>

                  {

                    service.description && (

                      <div

                        style={{

                          marginTop: 6,

                          color: "#666",

                          fontSize: 13,

                        }}

                      >

                        {service.description}

                      </div>

                    )

                  }

                </div>

              ),

            )

          }

        </div>

      </div>

      {/* ================================================= */}
      {/* CONTENT */}
      {/* ================================================= */}

      <div

        style={{

          padding: 32,

        }}

      >

        {

          selected && (

            <>

              <h2
                style={{
                  marginTop: 0,
                }}
              >

                {selected.title}

              </h2>

              <div

                style={{

                  color: "#666",

                  marginBottom: 28,

                }}

              >

                Выберите тип обращения

              </div>

              <div

                style={{

                  display: "grid",

                  gridTemplateColumns:
                    "repeat(auto-fill,minmax(260px,1fr))",

                  gap: 18,

                }}

              >

                {

                  selected.types.map(

                    type => (

                      <div

                        key={type.id}

                        onClick={() =>

                          void navigateAction(

                            "ticket:form",

                            {

                              service:
                                type.service,

                              type:
                                type.type,

                            },

                          )

                        }

                        style={{

                          border: "1px solid #ddd",

                          borderRadius: 12,

                          padding: 20,

                          cursor: "pointer",

                          transition: "all .2s",

                          background: "#fff",

                        }}

                        onMouseEnter={e => {

                          e.currentTarget.style.transform =
                            "translateY(-3px)"

                          e.currentTarget.style.borderColor =
                            "#2563eb"

                          e.currentTarget.style.boxShadow =
                            "0 10px 24px rgba(37,99,235,.12)"

                        }}

                        onMouseLeave={e => {

                          e.currentTarget.style.transform = ""

                          e.currentTarget.style.borderColor =
                            "#ddd"

                          e.currentTarget.style.boxShadow = ""

                        }}

                      >

                        <div

                          style={{

                            fontSize: 18,

                            fontWeight: 600,

                            marginBottom: 10,

                          }}

                        >

                          {type.title}

                        </div>

                        <div

                          style={{

                            color: "#666",

                            fontSize: 14,

                            lineHeight: 1.5,

                          }}

                        >

                          {

                            type.description ||

                            "Создать новую заявку"

                          }

                        </div>

                      </div>

                    ),

                  )

                }

              </div>

            </>

          )

        }

      </div>

    </div>

  )

}

export default TicketTypeSelect