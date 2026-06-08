# engine/changes/ChangeSet.py

class ChangeSet(list):

    def has(
        self,
        field,
    ):
        return any(
            x.field == field
            for x in self
        )

    def get(
        self,
        field,
    ):
        for item in self:

            if item.field == field:
                return item

        return None

    @property
    def changed_fields(self):

        return [
            x.field
            for x in self
        ]