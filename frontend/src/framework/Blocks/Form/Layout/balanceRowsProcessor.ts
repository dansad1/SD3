import type {
    FormBlock,
    FormFieldBlock,
} from "../types/types"

import type {
    FormLayoutConfig,
} from "../types/FormConfig"

import {
    registerFormLayoutProcessor,
} from "./registry"

import {
    resolveWidgetAlias,
    widgetRegistry,
} from "@/framework/components/dynamic/registry"


const GRID = 12


function getSpan(
    block: FormBlock,
): number {

    if (block.layout?.span) {
        return block.layout.span
    }

    if (block.type !== "field") {
        return 12
    }

    const field =
        block as FormFieldBlock


    const widgetKey =
        resolveWidgetAlias(
            field.field.widget
        )


    if (!widgetKey) {
        return 6
    }


    return (

        widgetRegistry[
            widgetKey
        ].layout
        ?.preferredSpan

        ??

        6

    )

}


registerFormLayoutProcessor(

    (
        blocks: FormBlock[],
        layout: FormLayoutConfig,
    ): FormBlock[] => {


        const strategy =

            layout.strategy

            ??

            "balance"


        if (

            strategy !==

            "balance"

        ) {

            return blocks

        }


        return balanceBlocks(

            blocks

        )

    }

)



function balanceBlocks(

    blocks: FormBlock[]

): FormBlock[] {


    const rows:
        FormBlock[][] = []
    let row:
        FormBlock[] = []
    let used = 0


    for (
        const block
        of blocks
    ) {


        const span =
            getSpan(
                block

            )


        if (

            row.length &&
            used + span >
            GRID

        ) {


            rows.push(
                balanceRow(
                    row

                )

            )

            row = []
            used = 0

        }


        row.push(
            block

        )
        used += span

    }


    if (

        row.length

    ) {

        rows.push(

            balanceRow(

                row

            )

        )

    }


    return rows.flat()

}



function balanceRow(

    row: FormBlock[]

): FormBlock[] {


    const normalized = row.map(

        block => ({

            ...block,

            layout: {

                ...(block.layout ?? {}),

                span: getSpan(

                    block

                ),

            },

        })

    )


    const total = normalized.reduce(

        (

            s,

            block

        ) =>

            s +

            (

                block.layout?.span

                ??

                6

            ),

        0

    )


    if (

        total >= GRID

    ) {

        return normalized

    }


    const free =

        GRID -

        total


    const extra =

        Math.floor(

            free /

            normalized.length

        )


    let remainder =

        free %

        normalized.length


    return normalized.map(

        block => {


            const current =

                block.layout?.span

                ??

                6


            let span =

                current +

                extra


            if (

                remainder >

                0

            ) {

                span++

                remainder--

            }


            return {

                ...block,


                layout: {

                    ...(

                        block.layout

                        ??

                        {}

                    ),


                    span,

                },

            }

        }

    )

}