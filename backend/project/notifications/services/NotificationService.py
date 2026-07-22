from backend.project.notifications.services.NotificationContextBuilder import (
    NotificationContextBuilder,
)
from backend.project.notifications.services.NotificationDispatcher import (
    NotificationDispatcher,
)
from backend.project.notifications.services.NotificationRecipientResolver import (
    NotificationRecipientResolver,
)
from backend.project.notifications.services.NotificationRuleResolver import (
    NotificationRuleResolver,
)


class NotificationService:

    @classmethod
    def trigger(
        cls,
        event_code,
        **kwargs,
    ):
        print("=" * 80)
        print("NOTIFICATION TRIGGER")
        print("event:", event_code)
        print("context keys:", list(kwargs.keys()))
        print("=" * 80)

        context = NotificationContextBuilder.build(
            **kwargs
        )

        rules = list(
            NotificationRuleResolver.get_rules(
                event_code,
            )
        )

        print(
            "NOTIFICATION RULES:",
            [
                rule.pk
                for rule in rules
            ],
        )

        results = []

        for rule in rules:
            recipients = (
                NotificationRecipientResolver.resolve(
                    rule=rule,
                    event_code=event_code,
                    context=context,
                )
            )

            print(
                "RULE:",
                rule.pk,
                "RECIPIENTS:",
                [
                    user.pk
                    for user in recipients
                ],
            )

            if not recipients:
                continue

            result = NotificationDispatcher.dispatch(
                rule=rule,
                context=context,
                recipients=recipients,
            )

            results.append(
                result
            )

        return results