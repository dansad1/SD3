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
        context = NotificationContextBuilder.build(
            **kwargs
        )

        rules = NotificationRuleResolver.get_rules(
            event_code
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

            if not recipients:
                results.append({
                    "rule": rule.pk,
                    "status": "skipped",
                    "reason": "no_recipients",
                })

                continue

            result = NotificationDispatcher.dispatch(
                rule=rule,
                context=context,
                recipients=recipients,
            )

            results.append({
                "rule": rule.pk,
                "status": "processed",
                "result": result,
            })

        return results