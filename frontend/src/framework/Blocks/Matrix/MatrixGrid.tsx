import type { MatrixData, MatrixCellSchema } from "./types"
import { MatrixCell } from "./MatrixCell"
import { getCellKey } from "./runtime/matrixKey"

type Props = {
  layout: MatrixData["layout"]
  cells: MatrixData["cells"]
  schema?: {
    cell?: MatrixCellSchema
  }
  onChange: (
    x: string,
    y: string,
    value: Partial<MatrixData["cells"][string]>
  ) => void
}

export const MatrixGrid = ({ layout, cells, schema, onChange }: Props) => {
  return (
    <div className="ui-matrix-wrapper">
      <div className="ui-matrix ui-matrix--attendance">
        <table className="ui-matrix-table">
          <thead>
            <tr>
              <th className="ui-matrix-sticky-top ui-matrix-sticky-left"></th>

              {layout.x.map(x => (
                <th key={x.id} className="ui-matrix-sticky-top">
                  {x.label}
                </th>
              ))}
            </tr>
          </thead>

          <tbody>
            {layout.y.map(y => (
              <tr key={y.id}>
                <th className="ui-matrix-sticky-left">
                  {y.label}
                </th>

                {layout.x.map(x => {
                  const key = getCellKey(x.id, y.id)
                  const value = cells[key] || {}

                  return (
                    <td key={key} className="ui-matrix-value">
                      <MatrixCell
                        schema={schema?.cell}
                        value={value}
                        onChange={patch =>
                          onChange(x.id, y.id, patch)
                        }
                      />
                    </td>
                  )
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}