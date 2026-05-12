// MultiSelect.tsx
import "@/Project/styles/select.css";

export interface Option {
  value: string | number;
  label: string;
}

interface MultiSelectProps {
  value: string[];                   // ВСЕГДА массив
  onChange: (value: string[]) => void;
  options: Option[];
  disabled?: boolean;
}

export default function MultiSelect({
  value,
  onChange,
  options,
  disabled = false,
}: MultiSelectProps) {

  const safeOptions = Array.isArray(options) ? options : [];

  function toggle(val: string) {
    if (value.includes(val)) {
      onChange(value.filter(v => v !== val));
    } else {
      onChange([...value, val]);
    }
  }

  return (
    <div className="ui-multiselect">
      {safeOptions.map(opt => (
        <label key={opt.value} className="ui-multiselect-item">
          <input
            type="checkbox"
            disabled={disabled}
            checked={value.includes(String(opt.value))}
            onChange={() => toggle(String(opt.value))}
          />
          <span>{opt.label}</span>
        </label>
      ))}
    </div>
  );
}
