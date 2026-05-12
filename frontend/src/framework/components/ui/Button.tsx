import type { ReactNode, ButtonHTMLAttributes } from "react";
import "@/Project/styles/button.css";

interface CustomButtonProps {
  variant?: "primary" | "secondary" | "danger" | "ghost";
  size?: "sm" | "md" | "lg";
  children: ReactNode;
}

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & CustomButtonProps;

export default function Button({
  children,
  variant = "primary",
  size = "md",
  className = "",
  type = "button",
  ...rest
}: ButtonProps) {
  return (
    <button
      type={type}
      {...rest}
      className={`ui-btn ui-btn-${variant} ui-btn-${size} ${className}`}
    >
      {children}
    </button>
  );
}