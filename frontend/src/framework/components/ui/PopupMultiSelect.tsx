import {
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react"

interface Option {
  value: string | number
  label: string
}

interface Props {
  value: string[]
  options: Option[]
  onChange: (value: string[]) => void
  disabled?: boolean
}

export default function PopupMultiSelect({
  value,
  options,
  onChange,
  disabled = false,
}: Props) {
  const [open, setOpen] = useState(false)
  const [search, setSearch] = useState("")
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handler = (event: MouseEvent) => {
      if (
        ref.current &&
        !ref.current.contains(event.target as Node)
      ) {
        setOpen(false)
      }
    }

    document.addEventListener("mousedown", handler)

    return () => {
      document.removeEventListener("mousedown", handler)
    }
  }, [])

  function toggle(optionValue: string) {
    if (disabled) {
      return
    }

    if (value.includes(optionValue)) {
      onChange(
        value.filter((item) => item !== optionValue)
      )
      return
    }

    onChange([...value, optionValue])
  }

  const filteredOptions = useMemo(() => {
    const query = search.trim().toLowerCase()

    if (!query) {
      return options
    }

    return options.filter((option) =>
      option.label.toLowerCase().includes(query)
    )
  }, [search, options])

  let displayText = "Выбрать…"

  if (value.length === 1) {
    const selectedOption = options.find(
      (option) => String(option.value) === value[0]
    )

    displayText = selectedOption?.label ?? ""
  } else if (value.length > 1 && value.length <= 3) {
    displayText = value
      .map((selectedValue) => {
        return (
          options.find(
            (option) =>
              String(option.value) === selectedValue
          )?.label ?? ""
        )
      })
      .filter(Boolean)
      .join(", ")
  } else if (value.length > 3) {
    displayText = `${value.length} выбрано`
  }

  return (
    <div
      ref={ref}
      style={{
        position: "relative",
        width: "100%",
      }}
    >
      <div
        className="ui-input"
        style={{
          cursor: disabled ? "not-allowed" : "pointer",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: 8,
          opacity: disabled ? 0.6 : 1,
        }}
        onClick={() => {
          if (!disabled) {
            setOpen((current) => !current)
          }
        }}
      >
        <span
          style={{
            flex: 1,
            minWidth: 0,
            overflow: "hidden",
            textOverflow: "ellipsis",
            whiteSpace: "nowrap",
          }}
        >
          {displayText}
        </span>

        <span
          aria-hidden="true"
          style={{
            flexShrink: 0,
            opacity: 0.6,
          }}
        >
          ▾
        </span>
      </div>

      {open && !disabled && (
        <div
          style={{
            position: "absolute",
            top: "100%",
            right: 0,
            zIndex: 999,
            width: 260,
            maxHeight: 340,
            marginTop: 4,
            padding: 10,
            overflowY: "auto",
            background: "white",
            border: "1px solid #ddd",
            borderRadius: 8,
            boxShadow: "0 4px 12px rgba(0, 0, 0, 0.15)",
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "flex-end",
              marginBottom: 6,
            }}
          >
            <button
              type="button"
              aria-label="Закрыть"
              onClick={() => setOpen(false)}
              style={{
                width: 28,
                height: 28,
                padding: 0,
                fontSize: 20,
                lineHeight: 1,
                cursor: "pointer",
                background: "transparent",
                border: 0,
              }}
            >
              ×
            </button>
          </div>

          <input
            type="text"
            value={search}
            onChange={(event) => {
              setSearch(event.target.value)
            }}
            placeholder="Поиск…"
            className="ui-input"
            style={{
              width: "100%",
              marginBottom: 8,
              boxSizing: "border-box",
            }}
          />

          {filteredOptions.length === 0 && (
            <div
              style={{
                padding: "8px 0",
                textAlign: "center",
                opacity: 0.6,
              }}
            >
              Ничего не найдено
            </div>
          )}

          <div
            style={{
              display: "flex",
              flexDirection: "column",
              gap: 2,
            }}
          >
            {filteredOptions.map((option) => {
              const optionValue = String(option.value)

              return (
                <label
                  key={optionValue}
                  style={{
                    display: "grid",
                    gridTemplateColumns: "20px minmax(0, 1fr)",
                    alignItems: "center",
                    columnGap: 8,
                    minHeight: 32,
                    padding: "4px 6px",
                    cursor: "pointer",
                    borderRadius: 4,
                  }}
                >
                  <input
                    type="checkbox"
                    checked={value.includes(optionValue)}
                    onChange={() => toggle(optionValue)}
                    style={{
                      width: 16,
                      height: 16,
                      margin: 0,
                      justifySelf: "center",
                    }}
                  />

                  <span
                    style={{
                      minWidth: 0,
                      lineHeight: 1.35,
                      overflowWrap: "anywhere",
                    }}
                  >
                    {option.label}
                  </span>
                </label>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}