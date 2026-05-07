from django.contrib.auth.base_user import (
    BaseUserManager
)


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(
        self,
        login,
        password=None,
        **extra_fields
    ):

        if not login:
            raise ValueError(
                "Login required"
            )

        user = self.model(
            login=login,
            **extra_fields
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(
            using=self._db
        )

        return user

    def create_superuser(
        self,
        login,
        password,
        **extra_fields
    ):

        extra_fields.setdefault(
            "is_staff",
            True
        )

        extra_fields.setdefault(
            "is_superuser",
            True
        )

        extra_fields.setdefault(
            "is_active",
            True
        )

        return self.create_user(
            login,
            password,
            **extra_fields
        )