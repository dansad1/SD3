import type { WidgetProps } from "../types"
import { BaseWidget } from "./Base"


type CommentValue = {
  text: string
  hide_from_client: boolean
}


function parseValue(
  value: unknown,
): CommentValue {

  if (
    value == null
    || value === ""
  ) {
    return {
      text: "",
      hide_from_client: false,
    }
  }

  if (typeof value === "string") {

    try {

      const parsed = JSON.parse(
        value,
      )

      return {
        text:
          parsed.text ?? "",

        hide_from_client:
          Boolean(
            parsed.hide_from_client,
          ),
      }

    } catch {

      return {
        text: value,
        hide_from_client: false,
      }

    }

  }

  if (
    typeof value === "object"
  ) {

    const parsed =
      value as Partial<CommentValue>

    return {

      text:
        parsed.text ?? "",

      hide_from_client:
        Boolean(
          parsed.hide_from_client,
        ),

    }

  }

  return {

    text: "",

    hide_from_client: false,

  }

}


export function CommentWidget({
  field,
  value,
  onChange,
  loading,
}: WidgetProps) {

  const disabled =
    Boolean(field.readonly)
    || Boolean(loading)

  const comment =
    parseValue(value)

  function update(
    text: string,
    hidden: boolean,
  ) {

    onChange(
      JSON.stringify({

        text,

        hide_from_client:
          hidden,

      }),
    )

  }

  return (

    <BaseWidget
      field={field}
      loading={loading}
    >

      <textarea

        className="ui-textarea"

        rows={5}

        disabled={disabled}

        value={comment.text}

        onChange={(e) =>

          update(

            e.target.value,

            comment.hide_from_client,

          )

        }

      />

      <label
        className="ui-checkbox"
      >

        <input

          type="checkbox"

          checked={
            comment.hide_from_client
          }

          disabled={disabled}

          onChange={(e) =>

            update(

              comment.text,

              e.target.checked,

            )

          }

        />

        <span>

          Скрыть от клиента

        </span>

      </label>

    </BaseWidget>

  )

}