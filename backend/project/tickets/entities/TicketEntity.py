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

        "list":
            "tickets.view",

        "view":
            "tickets.view",

        "create":
            "tickets.create",

        "edit":
            "tickets.edit",

        "delete":
            "tickets.delete",
    }

    # =====================================================
    # QUERYSET
    # =====================================================

    def get_select_related(self):

        return [

            field.name

            for field in (
                self.model._meta.get_fields()
            )

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

        fields = []

        for field in (

                self.model
                ._meta
                .get_fields()

        ):

            name = getattr(
                field,
                "name",
                None,
            )

            if not name:
                continue

            if not self.include_model_field(
                    field
            ):
                continue

            fields.append(

                DjangoField(
                    field
                )

            )

        existing_names = {

            field.name

            for field in fields

        }

        # =============================================
        # EXISTING TICKET
        # =============================================

        if obj is not None:

            dynamic_fields = (

                self.get_dynamic_fields(

                    request,

                    obj=obj,

                )

            )

        # =============================================
        # LIST MODE
        # =============================================

        else:

            fieldset = (

                TicketFieldSet.objects

                .filter(

                    code="default"

                )

                .first()

            )

            if fieldset:

                dynamic_fields = (

                    TicketField.objects

                    .filter(

                        fieldset=fieldset,

                    )

                    .order_by(


                        "id",

                    )

                )

            else:

                dynamic_fields = []

        for field in dynamic_fields:

            if (

                    field.name

                    in existing_names

            ):

                continue

            fields.append(

                DynamicField(

                    field

                )

            )

        return fields

    # =====================================================
    # DYNAMIC FIELDS
    # =====================================================

    def get_dynamic_fields(

            self,

            request,

            obj=None,

    ):

        fieldset = None

        # =============================================
        # EXISTING TICKET
        # =============================================

        if (

                obj

                and obj.type_id

                and obj.type

        ):

            fieldset = (

                obj.type.fieldset

            )

        # =============================================
        # CREATE MODE
        # =============================================

        else:

            type_id = request.GET.get(

                "type"

            )

            if not type_id:
                return []

            try:

                type_id = int(

                    type_id

                )

            except (

                    TypeError,

                    ValueError,

            ):

                return []

            ticket_type = (

                self.model

                ._meta

                .get_field(

                    "type"

                )

                .remote_field

                .model

                .objects

                .filter(

                    pk=type_id

                )

                .select_related(

                    "fieldset"

                )

                .first()

            )

            if ticket_type:

                fieldset = (

                    ticket_type.fieldset

                )

        if not fieldset:
            return []

        return (

            TicketField.objects

            .filter(

                fieldset=fieldset,

            )



        )

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def represent_option(

            self,

            obj,

    ):

        return {

            "value":

                obj.pk,

            "label":

                str(obj),

        }