def step_widget(ctx):
    # 🔥 если widget уже установлен — НЕ ТРОГАЕМ
    if "widget" in ctx.schema:
        return

    mapping = {
        "string": "TextInput",
        "text": "Textarea",
        "richtext": "RichText",
        "boolean": "Checkbox",
        "date": "DateInput",
        "datetime": "DateTimeInput",
        "foreignKey": "Select",
        "manyToMany": "MultiSelect",
        "json": "Textarea",
    }

    ctx.schema["widget"] = mapping.get(ctx.type, "TextInput")

    # html input type
    if ctx.schema["widget"] == "TextInput":
        ctx.schema["html_type"] = "text"