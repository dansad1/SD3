import { useEffect, type ReactNode } from "react";
import "@/Project/styles/modal.css";

interface ModalProps {
  isOpen: boolean;
  title?: string;
  children: ReactNode;
  onClose: () => void;
  width?: number | string;
  footer?: ReactNode;
}

export default function Modal({
  isOpen,
  title,
  children,
  onClose,
  width = 500,
  footer,
}: ModalProps) {
  // 🔒 Блокировка скролла фона
  useEffect(() => {
    if (!isOpen) return;

    const original = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    return () => {
      document.body.style.overflow = original;
    };
  }, [isOpen]);

  // ⌨ Закрытие по ESC
  useEffect(() => {
    if (!isOpen) return;

    const handleKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        onClose();
      }
    };

    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      className="ui-modal-overlay"
      onClick={onClose}
    >
      <div
        className="ui-modal"
        style={{
          width,
          maxWidth: "95vw", // mobile-safe
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="ui-modal-header">
          {title && <h3>{title}</h3>}

          <button
            type="button"
            className="ui-modal-close"
            onClick={onClose}
          >
            ×
          </button>
        </div>

        <div className="ui-modal-body">
          {children}
        </div>

        {footer && (
          <div className="ui-modal-footer">
            {footer}
          </div>
        )}
      </div>
    </div>
  );
}