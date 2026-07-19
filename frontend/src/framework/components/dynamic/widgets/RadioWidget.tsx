import type { WidgetRenderer } from "../types"
import { BaseWidget } from "./Base"


type RadioOption = {
    value: string | number | boolean
    label: string
}


export const RadioWidget: WidgetRenderer = (
    props,
) => {
    const {
        field,
        value,
        onChange,
        loading,
    } = props

    const options = (
        Array.isArray(field.options)
            ? field.options
            : []
    ) as RadioOption[]

    const currentValue = (
        value === null
        || value === undefined
            ? ""
            : String(value)
    )

    return (
        <BaseWidget
            field={field}
            loading={loading}
        >
            {({ disabled }) => (
                <div
                    role="radiogroup"
                    aria-label={field.label}
                    style={{
                        display: "flex",
                        flexWrap: "wrap",
                        gap: "8px",
                        width: "100%",
                    }}
                >
                    {options.map((option) => {
                        const optionValue = String(
                            option.value,
                        )

                        const checked = (
                            currentValue === optionValue
                        )

                        const optionId = [
                            "radio",
                            field.name,
                            optionValue,
                        ].join("-")

                        return (
                            <label
                                key={optionValue}
                                htmlFor={optionId}
                                style={{
                                    display: "inline-flex",
                                    alignItems: "center",
                                    justifyContent: "center",
                                    width: "auto",
                                    minWidth: "120px",
                                    minHeight: "42px",
                                    padding: "8px 14px",
                                    margin: 0,
                                    border: checked
                                        ? "1px solid #4f46e5"
                                        : "1px solid #d8deea",
                                    borderRadius: "10px",
                                    background: checked
                                        ? "#eef2ff"
                                        : "#ffffff",
                                    color: checked
                                        ? "#3730a3"
                                        : "#374151",
                                    fontWeight: checked
                                        ? 600
                                        : 400,
                                    cursor: disabled
                                        ? "not-allowed"
                                        : "pointer",
                                    opacity: disabled
                                        ? 0.6
                                        : 1,
                                    boxSizing: "border-box",
                                    userSelect: "none",
                                }}
                            >
                                <input
                                    id={optionId}
                                    type="radio"
                                    name={field.name}
                                    value={optionValue}
                                    checked={checked}
                                    disabled={disabled}
                                    onChange={() => {
                                        onChange(
                                            option.value,
                                        )
                                    }}
                                    style={{
                                        position: "absolute",
                                        width: "1px",
                                        height: "1px",
                                        padding: 0,
                                        margin: "-1px",
                                        overflow: "hidden",
                                        clip: "rect(0, 0, 0, 0)",
                                        whiteSpace: "nowrap",
                                        border: 0,
                                    }}
                                />

                                {option.label}
                            </label>
                        )
                    })}
                </div>
            )}
        </BaseWidget>
    )
}