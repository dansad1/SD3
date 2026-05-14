import DynamicField from "@/framework/components/dynamic/DynamicField"
import { OptionIterator } from "@/framework/components/dynamic/OptionIterator"

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

  // текущее поле
  onChange: (
    v: Json
  ) => void

  // 🔥 доступ к форме
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

  // ================= ERRORS =================

  const error =
    errors[0]

  // ================= OPTIONS =================

  const options =
    field.choices ?? []

  const isCheckboxList =
    Boolean(field.multiple) &&
    options.length > 0

  const normalizedValue =
    toValue(value)

  console.log(
    "🎯 FIELD RENDER",
    {
      name: field.name,
      widget: field.widget,
      rawValue: value,
      normalizedValue,
      errors,
    }
  )

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

        {isCheckboxList ? (

          <div className="ui-checkbox-list">

            <OptionIterator
              options={options}
              value={normalizedValue}
              multiple
              onChange={(v) =>
                onChange(v as Json)
              }
            >

              {(opt, ctx) => (

                <label
                  key={opt.value}
                  className="
                    ui-checkbox-item
                  "
                >

                  <input
                    type="checkbox"
                    checked={
                      ctx.checked
                    }
                    onChange={
                      ctx.toggle
                    }
                  />

                  <span>
                    {opt.label}
                  </span>

                </label>
              )}

            </OptionIterator>

          </div>

        ) : (

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

        )}

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