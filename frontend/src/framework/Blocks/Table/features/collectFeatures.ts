import type { TableApiBlock } from "../types/api"
import type { BaseRow } from "../types/runtime"
import { getTableFeatures } from "./registry"
import type { TableFeature } from "./types"

export function collectTableFeatures<T extends BaseRow>(
  block: TableApiBlock
): TableFeature<T>[] {

  const all =
    getTableFeatures() as TableFeature<T>[]

  return all.filter(feature => {

    /*
     * core
     */

    if (
      feature.name === "toolbar"
    ) {
      return true
    }

    /*
     * auto-enable bulkActions
     */

    if (
      feature.name === "bulkActions"
    ) {

      return Boolean(

        block.bulkActions?.length

        ||

        block.rowActions?.some(

          (action: any) =>

            action.bulk === true

        )

      )

    }

    /*
     * optional features
     */

    return !!block.features?.[

      feature.name as keyof
      typeof block.features

    ]

  })

}