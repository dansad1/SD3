from django.core.management.base import BaseCommand

from backend.project.users.models import (
    User,
    UserFieldSet,
)


class Command(BaseCommand):

    def handle(
        self,
        *args,
        **kwargs,
    ):
        root = User.objects.get(
            login="root",
        )

        print(root.fieldset)

        if root.fieldset is None:

            fieldset = UserFieldSet.objects.get(
                code="default",
            )

            root.fieldset = fieldset

            root.save(
                update_fields=[
                    "fieldset",
                ],
            )

            print("fieldset assigned")

        print(root.fieldset)