from django.core.exceptions import ValidationError


def validation_error_to_dict(error):
    if hasattr(error, "message_dict"):
        return error.message_dict

    if hasattr(error, "messages"):
        return {
            "__all__": error.messages
        }

    return {
        "__all__": [str(error)]
    }