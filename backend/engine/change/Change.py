# engine/changes/Change.py

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