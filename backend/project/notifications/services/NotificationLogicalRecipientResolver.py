class NotificationLogicalRecipientResolver:

    @classmethod
    def resolve(
        cls,
        logical_role,
        context,
    ):
        if logical_role == "target_user":
            user = context.get(
                "user",
            )

            return [
                user,
            ] if user else []

        if logical_role == "actor":
            user = context.get(
                "actor",
            )

            return [
                user,
            ] if user else []

        ticket = context.get(
            "ticket",
        )

        if not ticket:
            return []

        if logical_role == "requester":
            requester = ticket.get_value(
                "requester",
            )

            return [
                requester,
            ] if requester else []

        if logical_role == "assignee":
            executors = ticket.get_value(
                "executors",
            )

            return cls.normalize_users(
                executors,
            )

        if logical_role == "watcher":
            watchers = ticket.get_value(
                "watchers",
            )

            return cls.normalize_users(
                watchers,
            )

        return []

    @classmethod
    def normalize_users(
        cls,
        value,
    ):
        if not value:
            return []

        if isinstance(
            value,
            (list, tuple, set),
        ):
            return [
                user
                for user in value
                if user
            ]

        return [
            value,
        ]