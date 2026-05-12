import "@/Project/styles/checkbox.css"

interface CheckboxProps {
  checked: boolean;
  onChange: (v: boolean) => void;
  label?: string;
  disabled?: boolean;   // ✅ добавили
}

export default function Checkbox({
  checked,
  onChange,
  label,
  disabled = false,
}: CheckboxProps) {
  return (
    <label
      className={`ui-checkbox ${
        disabled ? "ui-checkbox-disabled" : ""
      }`}
    >
      <input
        type="checkbox"
        checked={!!checked}
        disabled={disabled}
        onChange={(e) => {
          if (disabled) return;
          onChange(e.target.checked);
        }}
      />
      {label && <span>{label}</span>}
    </label>
  );
}