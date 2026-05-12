import { useState, useRef, useEffect, useMemo } from "react";
import "@/Project/styles/select.css";

interface Option {
  value: string | number;
  label: string;
}

interface Props {
  value: string[];
  options: Option[];
  onChange: (v: string[]) => void;
  disabled?: boolean;   // ✅ добавили
}

export default function PopupMultiSelect({ value, options, onChange }: Props) {
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState("");
  const ref = useRef<HTMLDivElement>(null);

  // закрытие по клику вне
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  function toggle(val: string) {
    if (value.includes(val)) {
      onChange(value.filter((x) => x !== val));
    } else {
      onChange([...value, val]);
    }
  }

  // Фильтрация списка
  const filteredOptions = useMemo(() => {
    const q = search.trim().toLowerCase();
    if (!q) return options;

    return options.filter((o) => o.label.toLowerCase().includes(q));
  }, [search, options]);

  // Текст в поле
  let displayText = "Выбрать…";
  if (value.length === 1) {
    const one = options.find((o) => o.value == value[0]);
    displayText = one ? one.label : "";
  } else if (value.length > 1 && value.length <= 3) {
    displayText = value
      .map((v) => options.find((o) => o.value == v)?.label || "")
      .join(", ");
  } else if (value.length > 3) {
    displayText = `${value.length} выбрано`;
  }

  return (
    <div ref={ref} style={{ position: "relative", width: "100%" }}>
      {/* Поле */}
      <div
        className="ui-input"
        style={{
          cursor: "pointer",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
        onClick={() => setOpen(!open)}
      >
        <span
          style={{
            overflow: "hidden",
            textOverflow: "ellipsis",
            whiteSpace: "nowrap",
            flex: 1,
          }}
        >
          {displayText}
        </span>
        <span style={{ opacity: 0.6 }}>▾</span>
      </div>

      {/* Popover */}
      {open && (
        <div
          style={{
            position: "absolute",
            top: "100%",
            right: 0,
            zIndex: 999,
            background: "white",
            border: "1px solid #ddd",
            borderRadius: 8,
            marginTop: 4,
            padding: 10,
            width: 260,
            boxShadow: "0 4px 12px rgba(0,0,0,0.15)",
            maxHeight: 340,
            overflowY: "auto",
          }}
        >
          {/* Закрыть */}
          <div
            style={{
              textAlign: "right",
              fontSize: 20,
              cursor: "pointer",
              marginBottom: 6,
            }}
            onClick={() => setOpen(false)}
          >
            ×
          </div>

          {/* Поиск */}
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Поиск…"
            className="ui-input"
            style={{ marginBottom: 8 }}
          />

          {/* Список */}
          {filteredOptions.length === 0 && (
            <div style={{ padding: "6px 0", opacity: 0.6 }}>
              Ничего не найдено
            </div>
          )}

          {filteredOptions.map((opt) => (
            <label
              key={opt.value}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 6,
                padding: "4px 0",
                cursor: "pointer",
              }}
            >
              <input
                type="checkbox"
                checked={value.includes(String(opt.value))}
                onChange={() => toggle(String(opt.value))}
              />
              {opt.label}
            </label>
          ))}
        </div>
      )}
    </div>
  );
}
