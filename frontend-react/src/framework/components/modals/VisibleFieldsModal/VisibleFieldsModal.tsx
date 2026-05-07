import Button from "../../ui/Button";
import Checkbox from "../../ui/Checkbox";
import Modal from "../../ui/Modal";
import { useVisibleFieldsRuntime } from "./useVisibleFieldsRuntime";

interface Props {
  isOpen: boolean;
  onClose: () => void;
  onSaved: () => void;
  entity: string;
  fieldset?: string;
}

export default function VisibleFieldsModal({
  isOpen,
  onClose,
  onSaved,
  entity,
  fieldset = "default",
}: Props) {
  const {
    fields,
    loading,
    toggleField,
    save,
  } = useVisibleFieldsRuntime(entity, fieldset, isOpen);

  if (!isOpen) return null;

  return (
    <Modal
      title="Отображаемые поля"
      isOpen={isOpen}
      onClose={onClose}
      width={500}
      footer={
        <Button
          disabled={loading}
          onClick={async () => {
            await save();
            onSaved();
            onClose();
          }}
        >
          {loading ? "Сохраняем…" : "Сохранить"}
        </Button>
      }
    >
      {loading && <div>Загрузка…</div>}

      {!loading &&
        fields.map((f) => (
          <div key={f.key} style={{ marginBottom: 10 }}>
            <Checkbox
              checked={Boolean(f.selected)}
              onChange={(value) => toggleField(f.key, value)}
              label={f.label}
            />
          </div>
        ))}
    </Modal>
  );
}