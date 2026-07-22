from backend.project.notifications.services.NotificationService import (
    NotificationService,
)


class UserNotificationService:

    SPECIAL_FIELDS = {
        "is_active",
        "role",
        "password",
    }

    @classmethod
    def process(
        cls,
        *,
        target_user,
        created=False,
        changes=None,
        actor=None,
        password_changed=False,
    ):
        if hasattr(
            changes,
            "to_list",
        ):
            changes = changes.to_list()

        changes = changes or []

        print("=" * 80)
        print("USER NOTIFICATION PROCESS")
        print("user:", target_user.pk)
        print("created:", created)
        print("changes:", changes)
        print("password_changed:", password_changed)
        print("=" * 80)

        context = {
            "user": target_user,
            "actor": actor,
            "changes": changes,
        }

        # =================================================
        # CREATED
        # =================================================

        if created:

            print("TRIGGER: user.created")

            return NotificationService.trigger(
                "user.created",
                **context,
            )

        # =================================================
        # CHANGE MAP
        # =================================================

        change_map = {
            change.get("field"): change
            for change in changes
            if change.get("field")
        }

        results = []

        # =================================================
        # ACTIVE STATE
        # =================================================

        active_change = change_map.get(
            "is_active",
        )

        if active_change:

            event_code = (
                "user.activated"
                if target_user.is_active
                else "user.deactivated"
            )

            print(
                f"TRIGGER: {event_code}"
            )

            results.extend(
                NotificationService.trigger(
                    event_code,
                    **context,
                )
                or []
            )

        # =================================================
        # ROLE
        # =================================================

        if "role" in change_map:

            print(
                "TRIGGER: user.role_changed"
            )

            results.extend(
                NotificationService.trigger(
                    "user.role_changed",
                    **context,
                )
                or []
            )

        # =================================================
        # PASSWORD
        # =================================================

        if password_changed:

            print(
                "TRIGGER: user.password_changed"
            )

            results.extend(
                NotificationService.trigger(
                    "user.password_changed",
                    **context,
                )
                or []
            )

        # =================================================
        # OTHER CHANGES
        # =================================================

        ordinary_changes = [

            change

            for change in changes

            if change.get("field")
            not in cls.SPECIAL_FIELDS
        ]

        if ordinary_changes:

            ordinary_context = {
                **context,
                "changes": ordinary_changes,
            }

            print(
                "TRIGGER: user.changed"
            )

            results.extend(
                NotificationService.trigger(
                    "user.changed",
                    **ordinary_context,
                )
                or []
            )

        # =================================================
        # NO CHANGES
        # =================================================

        if not (
            active_change
            or "role" in change_map
            or password_changed
            or ordinary_changes
        ):

            print(
                "NOTIFICATION SKIPPED: no changes"
            )

            return None

        return results