import type { ChangeEvent } from "react";
import "@/Project/styles/select.css";

export interface Option {
  value: string | number;
  label: string;
}

interface SingleSelectProps {
  value: string | number;
  onChange: (value: string) => void;
  options: Option[];
  placeholder?: string;
  disabled?: boolean;
  className?: string;
}

export default function SingleSelect({
  value,
  onChange,
  options,
  placeholder = "— выберите —",
  disabled = false,
  className = "ui-input",
}: SingleSelectProps) {
  const safeOptions = Array.isArray(options) ? options : [];

  return (
    <select
      className={className}
      value={String(value ?? "")}
      disabled={disabled}
      onChange={(e: ChangeEvent<HTMLSelectElement>) =>
        onChange(e.target.value)
      }
    >
      <option key="__empty__" value="">
        {placeholder}
      </option>

      {safeOptions.map((opt) => (
        <option
          key={String(opt.value)}      // ✅ КЛЮЧЕВОЙ ФИКС
          value={String(opt.value)}    // ✅ всегда string
        >
          {opt.label}
        </option>
      ))}
    </select>
  );
}
