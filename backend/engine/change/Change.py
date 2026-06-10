from dataclasses import dataclass


@dataclass
class Change:

    field: str

    old_value: object

    new_value: object

    field_type: str | None = None

    label: str | None = None

    source: str = "field"

    @property
    def changed(self):
        return (
            self.old_value
            !=
            self.new_value
        )

    def to_dict(self):
        return {
            "field": self.field,
            "label": self.label,
            "old_value": self.old_value,
            "new_value": self.new_value,
            "field_type": self.field_type,
            "source": self.source,
        }