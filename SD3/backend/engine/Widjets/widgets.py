# core/api/widgets.py

import logging

logger = logging.getLogger(__name__)

WIDGET_MAP = {
    "text": "TextInput",
    "password": "PasswordInput",
    "email": "TextInput",
    "number": "NumberInput",
    "checkbox": "Checkbox",
    "textarea": "Textarea",
    "date": "DateInput",
    "datetime-local": "DateTimeInput",
    "file": "FileInput",
    "select": "Select",
    "multiselect": "MultiSelect",
    "time": "TimeInput",
    "richtext": "RichText",
}

def to_dsl_field(form_field):
    widget = form_field.widget
    input_type = getattr(widget, "input_type", "text")

    # textarea
    if widget.__class__.__name__ == "Textarea":
        input_type = "textarea"

    # select
    elif hasattr(form_field, "choices") and form_field.choices:
        if getattr(form_field, "multiple", False):
            input_type = "multiselect"
        else:
            input_type = "select"

    # date widget
    elif widget.__class__.__name__ in (
        "DateInput",
        "AdminDateWidget",
    ):
        input_type = "date"

    # time widget 👇
    elif widget.__class__.__name__ in (
        "TimeInput",
        "AdminTimeWidget",
    ):
        input_type = "time"

    # datetime widget
    elif widget.__class__.__name__ in (
        "DateTimeInput",
    ):
        input_type = "datetime-local"

    # ckeditor
    elif widget.__class__.__name__ in (
        "CKEditorWidget",
        "CKEditorUploadingWidget",
    ):
        input_type = "richtext"

    dsl_widget = WIDGET_MAP.get(input_type)

    if not dsl_widget:
        logger.warning(
            "Unknown input_type '%s' for field '%s'",
            input_type,
            form_field.name,
        )
        dsl_widget = "TextInput"

    data = {
        "id": form_field.name,
        "name": form_field.name,
        "label": form_field.label,
        "widget": dsl_widget,
        "required": form_field.required,
    }

    # html_type пробрасываем только для нативных input'ов
    if input_type not in (
        "text",
        "textarea",
        "select",
        "multiselect",
        "richtext",
    ):
        data["html_type"] = input_type

    # choices
    if hasattr(form_field, "choices") and form_field.choices:
        data["choices"] = [
            {
                "value": v,
                "label": l,
            }
            for v, l in form_field.choices
            if v != ""
        ]

    # readonly
    if widget.attrs.get("readonly"):
        data["readonly"] = True

    return data