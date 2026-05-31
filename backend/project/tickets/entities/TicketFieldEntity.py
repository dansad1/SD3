class TicketFieldEntity(
    BaseEntity
):

    model = TicketField

    entity = "ticket-fields"

    # =====================================================
    # FORM
    # =====================================================

    form_sections = [

        {
            "title": "Основное",

            "fields": [
                "fieldset",
                "name",
                "label",
                "field_type",
            ],
        },

        {
            "title": "UI",

            "fields": [
                "placeholder",
                "help_text",
                "default_value",
                "choices",
            ],
        },

        {
            "title": "Валидация",

            "fields": [
                "required",
                "unique",
                "regex",
                "min_value",
                "max_value",
            ],
        },

        {
            "title": "Отображение",

            "fields": [
                "show_in_list",
            ],
        },

        {
            "title": "Системное",

            "fields": [
                "is_multiple",
                "is_system",
            ],
        },
    ]

    # =====================================================
    # UI
    # =====================================================

    list_display = [

        "fieldset",

        "name",

        "label",

        "field_type",

        "required",

        "readonly",

        "hidden",

        "show_in_list",

        "order",
    ]

    search_fields = [
        "name",
        "label",
    ]

    filter_fields = [
        "fieldset",
        "field_type",
    ]

    ordering = [
        "fieldset",
        "order",
        "id",
    ]

    # =====================================================
    # ACCESS
    # =====================================================

    capabilities = {

        "list":
            "ticket_fields.view",

        "view":
            "ticket_fields.view",

        "create":
            "ticket_fields.create",

        "edit":
            "ticket_fields.edit",

        "delete":
            "ticket_fields.delete",
    }

    # =====================================================
    # QUERYSET
    # =====================================================

    def get_select_related(self):

        return [
            "fieldset",
        ]