import { DefaultPresentation }
from "./presentation/DefaultPresentation"

import { PickerPresentation }
from "./presentation/PickerPresentation"

import type {
    ActionBlock as ActionBlockType
}
from "./types"


type Props = ActionBlockType


export function ActionBlock(
    props: Props
){

    if(
        props.picker
    ){

        return (

            <PickerPresentation

                {...props}

            />

        )

    }


    return (

        <DefaultPresentation

            {...props}

        />

    )

}