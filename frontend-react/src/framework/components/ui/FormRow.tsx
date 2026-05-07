// src/components/ui/FormRow.tsx
import React from "react";
import "@/styles/Form.css";

interface FormRowProps extends React.HTMLAttributes<HTMLDivElement> {
  label?: string;
  children: React.ReactNode;
}

export default function FormRow({ label, children, className = "", ...rest }: FormRowProps) {
  return (
    <div className={`form-row ${className}`} {...rest}>
      {label && <label className="form-label">{label}</label>}
      <div className="form-field">{children}</div>
    </div>
  );
}
