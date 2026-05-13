def step_widget(ctx):

    mapping = {

        "string": {
            "widget": "TextInput",
            "html_type": "text",
        },

        # 🔥 PASSWORD SUPPORT
        "password": {
            "widget": "TextInput",
            "html_type": "password",
        },

        "text": {
            "widget": "Textarea",
        },

        "richtext": {
            "widget": "RichText",
        },

        "boolean": {
            "widget": "Checkbox",
        },

        "date": {
            "widget": "DateInput",
            "html_type": "date",
        },

        "datetime": {
            "widget": "DateTimeInput",
            "html_type": "datetime-local",
        },

        "foreignKey": {
            "widget": "Select",
        },

        "manyToMany": {
            "widget": "MultiSelect",
        },

        "json": {
            "widget": "Textarea",
        },
    }

    config = mapping.get(
        ctx.type,
        mapping["string"]
    )

    # =====================================
    # WIDGET
    # =====================================

    if "widget" not in ctx.schema:
        ctx.schema["widget"] = config["widget"]

    # =====================================
    # HTML TYPE
    # =====================================

    if (
        "html_type" not in ctx.schema
        and "html_type" in config
    ):
        ctx.schema["html_type"] = config["html_type"]