from django.core.exceptions import ValidationError

from backend.project.notifications.models import EmailSettings


class EmailSettingsValidationService:

    MIN_PORT = 1

    MAX_PORT = 65535

    DEFAULT_ENCRYPTION = EmailSettings.Encryption.TLS

    ALLOWED_ENCRYPTION = {
        EmailSettings.Encryption.NONE,
        EmailSettings.Encryption.TLS,
        EmailSettings.Encryption.SSL,
    }

    @classmethod
    def validate(
        cls,
        payload,
        instance=None,
    ):
        validated_payload = payload.copy()

        cls._validate_port(
            payload=validated_payload,
            instance=instance,
        )

        cls._validate_encryption(
            payload=validated_payload,
            instance=instance,
        )

        return validated_payload

    @classmethod
    def _validate_port(
        cls,
        payload,
        instance=None,
    ):
        port = cls._get_value(
            payload=payload,
            instance=instance,
            field_name="port",
        )

        try:
            port = int(port)
        except (
            TypeError,
            ValueError,
        ) as exc:
            raise ValidationError({
                "port": "Некорректный порт",
            }) from exc

        if not cls.MIN_PORT <= port <= cls.MAX_PORT:
            raise ValidationError({
                "port": (
                    f"Порт должен быть от "
                    f"{cls.MIN_PORT} до {cls.MAX_PORT}"
                ),
            })

        payload["port"] = port

    @classmethod
    def _validate_encryption(
        cls,
        payload,
        instance=None,
    ):
        encryption = cls._get_value(
            payload=payload,
            instance=instance,
            field_name="encryption",
            default=cls.DEFAULT_ENCRYPTION,
        )

        if encryption not in cls.ALLOWED_ENCRYPTION:
            raise ValidationError({
                "encryption": (
                    "Некорректный режим шифрования"
                ),
            })

        payload["encryption"] = encryption

    @staticmethod
    def _get_value(
        payload,
        instance,
        field_name,
        default=None,
    ):
        if field_name in payload:
            return payload[field_name]

        if instance is not None:
            return getattr(
                instance,
                field_name,
                default,
            )

        return default