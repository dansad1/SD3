from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.generic.models import (
    DynamicField,
    DjangoField,
)

from backend.project.tickets.models import (
    Ticket,
    TicketField,
    TicketFieldSet,
)


class TicketEntity(BaseEntity):

    model = Ticket

    entity = "tickets"

    # =====================================================
    # DEBUG
    # =====================================================

    def debug_queryset(
        self,
        title,
        queryset,
    ):
        print("=" * 80)
        print(title)
        print("MODEL:", queryset.model)
        print("LABEL:", queryset.model._meta.label)
        print(
            "FIELDS:",
            [
                f.name
                for f in queryset.model._meta.get_fields()
            ],
        )

        try:
            print("SQL:", queryset.query)
        except Exception as exc:
            print("SQL ERROR:", exc)

        print("=" * 80)

    # =====================================================
    # UI
    # =====================================================

    list_display = [
        "id",
        "type",
        "status",
        "priority",
        "company",
        "executor_group",
        "assigned_to",
        "created_at",
    ]

    search_fields = [
        "id",
    ]

    filter_fields = [
        "type",
        "status",
        "priority",
        "company",
        "executor_group",
        "assigned_to",
        "archived",
    ]

    # =====================================================
    # ACCESS
    # =====================================================

    capabilities = {
        "list": "tickets.view",
        "view": "tickets.view",
        "create": "tickets.create",
        "edit": "tickets.edit",
        "delete": "tickets.delete",
    }

    # =====================================================
    # QUERYSET
    # =====================================================

    def get_select_related(self):

        return [

            field.name

            for field in self.model._meta.get_fields()

            if (
                getattr(
                    field,
                    "many_to_one",
                    False,
                )
                and
                not field.auto_created
            )
        ]

    def get_prefetch_related(self):

        return [
            "dynamic_values",
            "dynamic_values__field",
        ]

    # =====================================================
    # FIELDS
    # =====================================================

    def get_fields(
        self,
        request,
        obj=None,
    ):

        print("\n")
        print("#" * 80)
        print("TicketEntity.get_fields()")
        print("OBJ:", obj)
        print("#" * 80)

        fields = []

        for field in self.model._meta.get_fields():

            name = getattr(
                field,
                "name",
                None,
            )

            if not name:
                continue

            if not self.include_model_field(field):
                continue

            fields.append(
                DjangoField(field)
            )

        existing_names = {
            field.name
            for field in fields
        }

        print("DJANGO FIELDS:", sorted(existing_names))

        # =================================================
        # EXISTING OBJECT
        # =================================================

        if obj is not None:

            print("MODE: EDIT")

            dynamic_fields = self.get_dynamic_fields(
                request,
                obj=obj,
            )

        # =================================================
        # CREATE / LIST
        # =================================================

        else:

            print("MODE: CREATE/LIST")

            fieldset = (
                TicketFieldSet.objects
                .filter(
                    code="default",
                )
                .first()
            )

            print("FIELDSET:", fieldset)

            if fieldset:

                print(
                    "FIELDSET MODEL:",
                    fieldset._meta.label,
                )

                print(
                    "FIELDSET CLASS:",
                    fieldset.__class__,
                )

                print(
                    "RELATED MODEL:",
                    fieldset.fields.model,
                )

                qs = (
                    TicketField.objects
                    .filter(
                        fieldset=fieldset,
                    )
                    .order_by("id")
                )

                self.debug_queryset(
                    "TicketField queryset",
                    qs,
                )

                dynamic_fields = qs

            else:

                print("NO DEFAULT FIELDSET")

                dynamic_fields = []

        print(
            "DYNAMIC COUNT:",
            len(dynamic_fields),
        )

        for field in dynamic_fields:

            print(
                "FIELD:",
                field.name,
                field.field_type,
            )

            if field.name in existing_names:
                print(
                    "SKIP:",
                    field.name,
                    "(already exists)",
                )
                continue

            fields.append(
                DynamicField(field)
            )

        print(
            "FINAL:",
            [f.name for f in fields],
        )

        return fields

    # =====================================================
    # DYNAMIC
    # =====================================================

    def get_dynamic_fields(
        self,
        request,
        obj=None,
    ):

        print("\n")
        print("=" * 80)
        print("get_dynamic_fields()")
        print("=" * 80)

        fieldset = None

        if (
            obj
            and obj.type_id
            and obj.type
        ):

            print("MODE: EDIT")

            print("TYPE:", obj.type)
            print(
                "TYPE MODEL:",
                obj.type._meta.label,
            )

            fieldset = obj.type.fieldset

        else:

            print("MODE: CREATE")

            type_id = request.GET.get(
                "type",
            )

            print("REQUEST TYPE:", type_id)

            if not type_id:
                print("NO TYPE")
                return []

            try:

                type_id = int(type_id)

            except (
                TypeError,
                ValueError,
            ):

                print("INVALID TYPE")
                return []

            ticket_type = (
                self.model
                ._meta
                .get_field("type")
                .remote_field
                .model
                .objects
                .filter(
                    pk=type_id,
                )
                .select_related(
                    "fieldset",
                )
                .first()
            )

            print("TICKET TYPE:", ticket_type)

            if ticket_type:

                fieldset = (
                    ticket_type.fieldset
                )

        if not fieldset:

            print("NO FIELDSET")
            return []

        print("FIELDSET:", fieldset)

        print(
            "FIELDSET MODEL:",
            fieldset._meta.label,
        )

        print(
            "FIELDSET CLASS:",
            fieldset.__class__,
        )

        print(
            "RELATED MODEL:",
            fieldset.fields.model,
        )

        qs = (
            TicketField.objects
            .filter(
                fieldset=fieldset,
            )
            .order_by("id")
        )

        self.debug_queryset(
            "Dynamic queryset",
            qs,
        )

        return qs

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def represent_option(
        self,
        obj,
    ):

        return {
            "value": obj.pk,
            "label": str(obj),
        }