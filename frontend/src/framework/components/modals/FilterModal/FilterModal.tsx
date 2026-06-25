import { FieldRenderer } from "@/framework/Blocks/Form/render/FieldRenderer"
import Button from "../../ui/Button"
import Modal from "../../ui/Modal"



import { useFilterRuntime }
  from "./useFilterRuntime"


interface Props {

  isOpen: boolean

  onClose: () => void

  onApply?: (
    query: Record<string, string>
  ) => void

  entity: string

  fieldset?: string
    onSaved?: () => void

}


export default function FilterModal({

  isOpen,

  onClose,

  onApply,

  entity,

  fieldset = "default",

}: Props) {

console.log(
    "FilterModal",
    isOpen,
  )
  const {

    loading,

    fields,

    values,

    setValues,

    setFieldValue,

    buildEmptyValues,

    buildQuery,

  } = useFilterRuntime(

    entity,

    fieldset,

    {},

  )


  if (!isOpen) {
    return null
  }


  return (

    <Modal

      title="Фильтр"

      isOpen={isOpen}

      onClose={onClose}

      width={900}


      footer={

        <>

          <Button

            variant="secondary"

            onClick={() => {

              setValues(

                buildEmptyValues(

                  fields,

                )

              )

            }}

          >

            Сбросить

          </Button>


          <Button

            onClick={() => {

              onApply?.(

                buildQuery(),

              )

              onClose()

            }}

          >

            Применить

          </Button>

        </>

      }

    >

      {

        loading

        &&

        <div>

          Загрузка...

        </div>

      }


      {

        !loading

        &&

        <div

          style={{

            display:

              "grid",

            gridTemplateColumns:

              "220px 1fr",

            gap:

              12,

          }}

        >

          {

            fields.map(

              field => (

                <FieldRenderer

                  key={

                    field.id

                  }

                  field={

                    field

                  }

                  value={

                    values[
                      field.name
                    ]

                  }

                  errors={[]}

                  onChange={

                    value => {

                      setValues(

                        prev => ({

                          ...prev,

                          [

                            field.name

                          ]:

                          value,

                        })

                      )

                    }

                  }

                  setFieldValue={

                    setFieldValue

                  }

                />

              )

            )

          }

        </div>

      }

    </Modal>

  )

}