import type {
  BaseRow,
} from "../types/runtime"

import type {
  TableFeature,
} from "./types"


export function paginationFeature<

  T extends BaseRow

>(): TableFeature<T> {

  return {

    name:
      "pagination",

    phase:
      "afterList",


    apply(ctx) {
console.log("PAGINATION APPLY")

    console.log(
        "LIST",
        ctx.list
    )

    console.log(
        "PAGE",
        ctx.list?.page
    )

      const page =

        ctx.list?.page


      if (

        !page

      ) {

        return ctx

      }


      return {

        ...ctx,


        ctrl: {


          ...ctx.ctrl,


          pagination: {


            page:

              page.page,


            pages:

              page.pages,


            total:

              page.total,


            pageSize:

              page.page_size,


            setPage(

              nextPage:
                number

            ) {

              ctx.query
                .setPage(

                  nextPage

                )

            },

          },

        },

      }

    },

  }

}