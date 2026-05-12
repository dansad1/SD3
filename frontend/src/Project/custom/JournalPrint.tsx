/* eslint-disable @typescript-eslint/no-explicit-any */
import { useEffect, useMemo, useState } from "react"

// =========================
// CSRF helper
// =========================


const JournalPrint = ({ week_offset, mode }: any) => {
  const [data, setData] = useState<any>(null)

  // =========================
  // LOAD DATA
  // =========================
 useEffect(() => {
  let active = true

  const load = async () => {
    const res = await fetch(
      `/api/resource/journal.print/?week_offset=${week_offset}&mode=${mode}`,
      {
        credentials: "include",
      }
    )

    if (!res.ok) {
      const text = await res.text()
      console.error("API ERROR:", text)
      return
    }

    const json = await res.json()

    if (active) setData(json)
  }

  load()

  return () => {
    active = false
  }
}, [week_offset, mode])

  // =========================
  // OPTIMIZATION
  // =========================
  const cellMap = useMemo(() => {
    if (!data) return {}

    const map: Record<string, any> = {}

    data.columns.forEach((day: any, dIdx: number) => {
      day.slots.forEach((slot: any, sIdx: number) => {
        slot.rows.forEach((row: any) => {
          const key = `${row.student.id}-${dIdx}-${sIdx}`
          map[key] = row
        })
      })
    })

    return map
  }, [data])

  if (!data) return <div>Loading...</div>

  const { students, columns, start, end, group, monthly } = data

  return (
    <div className="journal-print">

      {/* BUTTON */}
      <button
        className="jp-print-btn"
        onClick={() => window.print()}
      >
        🖨 Печать
      </button>

      {/* HEADER */}
      <h3 className="jp-title">
        Группа № {group}
        <br />
        {monthly
          ? <>Журнал за {start}</>
          : <>Журнал с {start} по {end}</>
        }
      </h3>

      {/* TABLE */}
      <div className="jp-scroll">
        <table className="jp-table">

          <thead>
            <tr>
              <th className="jp-student">
                Фамилия, имя
              </th>

              {columns.map((day: any, i: number) => (
                <th key={i} colSpan={6}>
                  {day.date} — {day.day_name}
                </th>
              ))}
            </tr>

            <tr>
              <th></th>

              {columns.map((day: any, dIdx: number) =>
                day.slots.map((slot: any, sIdx: number) => (
                  <th key={`${dIdx}-${sIdx}`} className="jp-slot">
                    {slot.discipline && (
                      <div className="jp-vertical">
                        {slot.discipline}
                      </div>
                    )}
                  </th>
                ))
              )}
            </tr>
          </thead>

          <tbody>
            {students.map((student: any) => (
              <tr key={student.id}>
                <td className="jp-student">
                  {student.username}
                </td>

                {columns.map((day: any, dIdx: number) =>
                  day.slots.map((_, sIdx: number) => {
                    const key = `${student.id}-${dIdx}-${sIdx}`
                    const row = cellMap[key]

                    return (
                      <td key={key} className="jp-cell">
                        {row?.attended && "+"}

                        {row?.grade && (
                          <div className="jp-grade">
                            {row.grade}
                          </div>
                        )}
                      </td>
                    )
                  })
                )}
              </tr>
            ))}
          </tbody>

        </table>
      </div>

      <div className="jp-sign">
        Староста ___________________________<br />
        Куратор ____________________________
      </div>

    </div>
  )
}

export default JournalPrint