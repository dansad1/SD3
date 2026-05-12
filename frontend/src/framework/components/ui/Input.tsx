import { useState } from "react";
import type { InputHTMLAttributes, ChangeEvent, ReactNode } from "react";
import "@/Project/styles/input.css";

interface InputProps
  extends Omit<InputHTMLAttributes<HTMLInputElement>, "onChange" | "value"> {
  value: string;
  onChange: (value: string) => void;
  icon?: ReactNode;
  error?: string;
}

export default function Input({
  value,
  onChange,
  type = "text",
  placeholder,
  icon,
  error,
  ...rest
}: InputProps) {
  const [showPassword, setShowPassword] = useState(false);

  const isPassword = type === "password";
  const realType = isPassword && showPassword ? "text" : type;

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    onChange(e.target.value);
  };

  return (
    <div className="ui-input-wrap">
      {icon && <span className="ui-input-icon">{icon}</span>}

      <input
        {...rest}
        className={`ui-input ${error ? "ui-input-error" : ""}`}
        type={realType}
        value={value}
        placeholder={placeholder}
        onChange={handleChange}
      />

      {isPassword && (
        <span
          className="ui-password-eye"
          onClick={() => setShowPassword(!showPassword)}
        >
          {showPassword ? "🙈" : "👁️"}
        </span>
      )}

      {error && <div className="ui-error-text">{error}</div>}
    </div>
  );
}
