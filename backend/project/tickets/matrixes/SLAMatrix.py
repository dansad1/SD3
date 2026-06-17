# backend/project/tickets/matrixes/SLAMatrix.py

from backend.engine.matrix.Base.BaseMatrix import (
    BaseMatrix,
)

from backend.project.tickets.models import (
    TicketSLA,
    TicketType,
    TicketPriority,
)


class SLAMatrix(
    BaseMatrix
):

    class Meta:

        code = "ticket-slas"

        capabilities = {

            "view":
                "ticket_slas.view",

            "edit":
                "ticket_slas.edit",
        }

    # =====================================================
    # SCHEMA
    # =====================================================

    def build_schema(
        self,
        request,
    ):
        types = list(
            TicketType.objects.order_by(
                "name",
            )
        )

        priorities = list(
            TicketPriority.objects.order_by(
                "level",
                "name",
            )
        )

        return {

            "value_type":
                "number",

            "min":
                0,

            "step":
                1,

            "rows": [

                {
                    "id":
                        ticket_type.id,

                    "label":
                        str(ticket_type),
                }

                for ticket_type in types
            ],

            "columns": [

                {
                    "id":
                        priority.id,

                    "label":
                        str(priority),
                }

                for priority in priorities
            ],
        }

    # =====================================================
    # DATA
    # =====================================================

    def load_data(
        self,
        request,
    ):
        return {

            "items": [

                {
                    "row":
                        sla.type_id,

                    "column":
                        sla.priority_id,

                    "value":
                        sla.hours,
                }

                for sla in (

                    TicketSLA.objects

                    .select_related(
                        "type",
                        "priority",
                    )
                )
            ],
        }

    # =====================================================
    # SAVE
    # =====================================================

    def save_changes(
        self,
        request,
        changes,
    ):

        for change in changes:

            # -----------------------------------------
            # SUPPORT OLD AND NEW API
            # -----------------------------------------

            type_id = (

                change.get(
                    "row"
                )

                or

                change.get(
                    "y"
                )
            )

            priority_id = (

                change.get(
                    "column"
                )

                or

                change.get(
                    "x"
                )
            )

            raw_value = change.get(
                "value"
            )

            if isinstance(
                raw_value,
                dict,
            ):
                value = raw_value.get(
                    "value"
                )

            else:
                value = raw_value

            # -----------------------------------------
            # DELETE
            # -----------------------------------------

            if value in (
                None,
                "",
            ):

                TicketSLA.objects.filter(

                    type_id=
                    type_id,

                    priority_id=
                    priority_id,

                ).delete()

                continue

            # -----------------------------------------
            # PARSE
            # -----------------------------------------

            try:

                hours = int(
                    value
                )

            except (

                TypeError,

                ValueError,

            ):

                continue

            if hours < 0:

                hours = 0

            # -----------------------------------------
            # UPSERT
            # -----------------------------------------

            TicketSLA.objects.update_or_create(

                type_id=
                type_id,

                priority_id=
                priority_id,

                defaults={

                    "hours":
                        hours,

                },
            )

        return {

            "success":
                True,
        }