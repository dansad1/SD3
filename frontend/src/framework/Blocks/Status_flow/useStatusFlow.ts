
import { useResourceDataSource } from "../Data/sources/useResourceDataSource"
import type {
    StatusFlowData,
} from "./types"


export function useStatusFlow(
    source: string,
) {

    const {

        data,

        loading,

    } = useResourceDataSource<StatusFlowData>({
        data: `resource:${source}`,
    })


    return {
        data,
        loading,
        error: null,

    }

}