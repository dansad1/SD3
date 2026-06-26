import { useSearchParams } from "react-router-dom"



export function useTableQueryRuntime() {

  const [
    params,
    setParams,
  ] = useSearchParams()


  const page = Number(

    params.get("page")

    ?? 1

  )


  const sort = (

    params.get(

      "sort"

    )

    ?? undefined

  )


  const search = (

    params.get(

      "q"

    )

    ?? ""

  )


  const filters = Object.fromEntries(

    [...params.entries()]

      .filter(

        ([key]) =>

          ![

            "page",

            "sort",

            "q",

          ].includes(

            key,

          )

      )

  )


  const updateParams = (

    updater: (

      p: URLSearchParams

    ) => void

  ) => {

    const next = new URLSearchParams(

      params

    )

    updater(

      next

    )

    setParams(

      next

    )

  }


  const setPage = (

    p: number

  ) => {

    updateParams(

      next => {

        next.set(

          "page",

          String(

            p

          )

        )

      }

    )

  }


  const setSort = (

    s: string

  ) => {

    updateParams(

      next => {

        next.set(

          "sort",

          s,

        )

        next.set(

          "page",

          "1",

        )

      }

    )

  }


  const setSearch = (

    q: string

  ) => {

    updateParams(

      next => {

        if (

          q

        ) {

          next.set(

            "q",

            q,

          )

        }

        else {

          next.delete(

            "q"

          )

        }

        next.set(

          "page",

          "1",

        )

      }

    )

  }


  const setFilters = (

    values: Record<

      string,

      string

    >

  ) => {

    updateParams(

      next => {


        // удалить старые


        for (

          const key

          of [

            ...next.keys()

          ]

        ) {

          if (

            ![

              "page",

              "sort",

              "q",

            ].includes(

              key

            )

          ) {

            next.delete(

              key

            )

          }

        }


        // добавить новые


        for (

          const [

            key,

            value,

          ]

          of Object.entries(

            values

          )

        ) {

          if (

            value

          ) {

            next.set(

              key,

              value,

            )

          }

        }


        next.set(

          "page",

          "1",

        )

      }

    )

  }


  return {

    page,

    sort,

    search,

    filters,


    params,


    setPage,

    setSort,

    setSearch,

    setFilters,

  }

}