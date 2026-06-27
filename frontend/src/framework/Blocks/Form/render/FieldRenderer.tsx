import DynamicField from "@/framework/components/dynamic/DynamicField"

import type {
  FieldSchema,
  Value,
} from "@/framework/components/dynamic/types"

import type { Json }
  from "@/framework/types/json"

/* ================= COMMAND ================= */

type FieldCommand = {
  targetField: string
  value: string
  mode: "append" | "replace"
}

function isCommand(
  v: unknown
): v is FieldCommand {

  return (
    typeof v === "object" &&
    v !== null &&
    "targetField" in v &&
    "value" in v &&
    "mode" in v
  )
}

/* ================= conversions ================= */

type ValueObject = {
  value:
    | string
    | number
    | null

  label?: string
}

function isValueObject(
  v: unknown
): v is ValueObject {

  return (
    typeof v === "object" &&
    v !== null &&
    "value" in v
  )
}

function toValue(
  value: Json
): Value {

  if (
    value === null ||
    value === undefined
  ) {
    return null
  }

  if (isValueObject(value)) {

    const v = value.value

    return v == null
      ? null
      : String(v)
  }

  if (
    typeof value === "number"
  ) {
    return String(value)
  }

  return value as Value
}

function toJson(
  value: Value
): Json {

  if (value instanceof File) {
    return null
  }

  return value as Json
}

/* ================= types ================= */

type Props = {

  field: FieldSchema

  value: Json

  errors?: string[]

  onChange: (
    v: Json
  ) => void

  setFieldValue: (
    name: string,
    updater: (
      prev: Json
    ) => Json
  ) => void
}

/* ================= component ================= */

export function FieldRenderer({

  field,

  value,

  errors = [],

  onChange,

  setFieldValue,

}: Props) {

  const error =
    errors[0]

  const normalizedValue =
    toValue(value)

  

  return (

    <div
      className={
        error
          ? "form-field has-error"
          : "form-field"
      }
    >

      {/* ================= LABEL ================= */}

      {field.label && (

        <label className="form-label">

          {field.label}

          {field.required &&
            " *"}

        </label>

      )}

      {/* ================= INPUT ================= */}

      <div className="form-input">

        <DynamicField

          field={field}

          value={
            normalizedValue
          }

          onChange={(v) => {

            // ================= COMMAND =================

            if (isCommand(v)) {

              const {
                targetField,
                value,
                mode,
              } = v

              setFieldValue(
                targetField,
                (prev) => {

                  const prevStr =
                    typeof prev ===
                    "string"
                      ? prev
                      : ""

                  if (
                    mode ===
                    "append"
                  ) {

                    return (
                      prevStr +
                      value
                    ) as Json
                  }

                  return value as Json
                }
              )

              return
            }

            // ================= NORMAL =================

            onChange(
              toJson(v)
            )

          }}

        />

      </div>

      {/* ================= ERROR ================= */}

      {error && (

        <div
          className="
            form-error-text
          "
        >
          {error}
        </div>

      )}

      {/* ================= HELP ================= */}

      {field.help_text && (

        <div className="form-help">

          {field.help_text}

        </div>

      )}

    </div>
  )
}