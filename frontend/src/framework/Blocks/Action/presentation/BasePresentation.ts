import type { ReactNode } from "react"

export type PresentationProps = {

    children: ReactNode

}

export interface ActionPresentation {

    render(

        props: PresentationProps

    ): ReactNode

}