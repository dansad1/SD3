type Props = {

    page: number

    pages: number

    total: number

    pageSize: number

    onChange: (
        page: number,
    ) => void

}


export function Pagination({

    page,

    pages,

    total,

    pageSize,

    onChange,

}: Props) {


    const items: Array<
        number | "..."
    > = []


    if (pages <= 7) {

        for (

            let i = 1;

            i <= pages;

            i++

        ) {

            items.push(i)

        }

    }

    else {

        items.push(1)


        const start = Math.max(

            2,

            page - 1,

        )


        const end = Math.min(

            pages - 1,

            page + 1,

        )


        if (start > 2) {

            items.push("...")

        }


        for (

            let i = start;

            i <= end;

            i++

        ) {

            items.push(i)

        }


        if (

            end < pages - 1

        ) {

            items.push("...")

        }


        items.push(

            pages

        )

    }


    const shown = Math.max(

        0,

        Math.min(

            pageSize,

            total -

            (

                (page - 1)

                * pageSize

            )

        )

    )


    return (

        <div

            className=

                "ui-pagination"

        >


            <button

                className=

                    "ui-btn ui-btn-secondary"


                disabled={

                    page <= 1

                }


                onClick={() =>

                    onChange(

                        Math.max(

                            1,

                            page - 1,

                        )

                    )

                }

            >

                ‹‹

            </button>



            {

                items.map(

                    (

                        item,

                        index,

                    ) => {


                        if (

                            item ===

                            "..."

                        ) {

                            return (

                                <span

                                    key={

                                        `ellipsis-${

                                            index

                                        }`

                                    }

                                >

                                    ...

                                </span>

                            )

                        }


                        return (

                            <button

                                key={

                                    `page-${

                                        item

                                    }-${

                                        index

                                    }`

                                }


                                className={

                                    item === page

                                        ?

                                        "ui-btn ui-btn-primary"

                                        :

                                        "ui-btn ui-btn-secondary"

                                }


                                onClick={() =>

                                    onChange(

                                        item

                                    )

                                }

                            >

                                {

                                    item

                                }

                            </button>

                        )

                    }

                )

            }


            <button

                className=

                    "ui-btn ui-btn-secondary"


                disabled={

                    page >= pages

                }


                onClick={() =>

                    onChange(

                        Math.min(

                            pages,

                            page + 1,

                        )

                    )

                }

            >

                ››

            </button>


            <span>

                На странице

                {" "}

                <b>

                    {

                        shown

                    }

                </b>


                {" "}

                · Всего

                {" "}

                <b>

                    {

                        total

                    }

                </b>

            </span>

        </div>

    )

}