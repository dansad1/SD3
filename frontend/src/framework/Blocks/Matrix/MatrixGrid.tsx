import type {
  MatrixData,
  MatrixSchema,
  MatrixCellSchema,
} from "./types"
import { MatrixCell } from "./MatrixCell"
import { getCellKey } from "./runtime/matrixKey"

type Props = {
  layout: MatrixData["layout"]
  cells: MatrixData["cells"]
  schema?: MatrixSchema

  onChange: (
    x: string,
    y: string,
    value: Partial<MatrixData["cells"][string]>
  ) => void
}

function getCellSchema(
  schema: MatrixSchema | undefined,
  x: string,
  y: string,
): MatrixCellSchema | undefined {

  if (!schema) {
    return undefined
  }

  const key = getCellKey(x, y,)
  return (
    schema.cells?.[key]??
    schema.columns?.[x]??
    schema.rows?.[y]??
    schema.defaultCell
  )

}


export const MatrixGrid = ({
  layout,
  cells,
  schema,
  onChange,
}: Props) => {
  return (
    <div className="ui-matrix-wrapper">
      <div className="ui-matrix ui-matrix--attendance">
        <table className="ui-matrix-table">
          <thead>
            <tr>
              <th
                className="ui-matrix-sticky-top ui-matrix-sticky-left"
              />
              {layout.x.map(x => (
                <th
                  key={x.id}
                  className="ui-matrix-sticky-top"
                >
                  {x.label}
                </th>
              ))}
            </tr>
          </thead>

          <tbody>
            {layout.y.map(y => (
              <tr key={y.id}>
                <th
                  className="ui-matrix-sticky-left"
                >
                  {y.label}

                </th>
                {layout.x.map(x => {
                  const key = getCellKey(x.id,y.id,)
                  const value = (cells[key]||{})
                  const cellSchema = getCellSchema(schema,x.id, y.id,)
                  return (
                    <td
                      key={key}
                      className="ui-matrix-value"
                    >
                      <MatrixCell

                        schema={cellSchema}
                        value={value}
                        onChange={patch =>
                          onChange(
                            x.id,
                            y.id,
                            patch,
      )

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