from backend.project.tickets.models import (
    TicketField,
    TicketFieldSet,
    TicketType,
)


class TicketFieldService:

    # =====================================================
    # PAYLOAD
    # =====================================================

    @classmethod
    def get_type_id(
        cls,
        request,
    ):

        payload = getattr(
            request,
            "_form_payload",
            {},
        ) if request else {}

        if payload:

            value = payload.get(
                "type",
            )

            if hasattr(
                value,
                "pk",
            ):
                return value.pk

            if isinstance(
                value,
                dict,
            ):
                return value.get(
                    "value",
                )

            return value

        if request:

            return request.GET.get(
                "type",
            )

        return None

    # =====================================================
    # FIELDSET
    # =====================================================

    @classmethod
    def get_default_fieldset(
        cls,
    ):
        return (

            TicketFieldSet.objects

            .filter(
                code="default",
                is_active=True,
            )

            .first()

        )

    @classmethod
    def get_type_fieldset(
        cls,
        type_id,
    ):

        try:

            type_id = int(
                type_id,
            )

        except (
            TypeError,
            ValueError,
        ):

            return None

        ticket_type = (

            TicketType.objects

            .select_related(
                "fieldset",
            )

            .filter(
                pk=type_id,
            )

            .first()

        )

        if not ticket_type:
            return None

        return ticket_type.fieldset

    # =====================================================
    # FIELDS
    # =====================================================

    @classmethod
    def get_fields_for_fieldset(
        cls,
        fieldset,
    ):

        if not fieldset:
            return []

        return (

            TicketField.objects

            .filter(
                fieldset=fieldset,
            )

            .order_by(
                "id",
            )

        )

    @classmethod
    def get_fields(
        cls,
        request,
        ticket=None,
    ):

        # =================================================
        # EDIT
        # =================================================

        if (
            ticket
            and ticket.type_id
        ):

            return cls.get_fields_for_fieldset(
                ticket.type.fieldset,
            )

        # =================================================
        # CREATE
        # =================================================

        type_id = cls.get_type_id(
            request,
        )

        if not type_id:

            return cls.get_fields_for_fieldset(

                cls.get_default_fieldset()

            )

        return cls.get_fields_for_fieldset(

            cls.get_type_fieldset(
                type_id,
            )

        )