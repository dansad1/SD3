from django.contrib.auth import user_logged_in
from django.dispatch import receiver

from backend.project.audit.auth.get_ip import get_ip
from backend.project.audit.models.AuthJournal import AuthJournal


@receiver(user_logged_in)
def on_login(sender, request, user, **kwargs):

    AuthJournal.objects.create(
        user=user,
        action="login",
        ip=get_ip(request),
        user_agent=request.META.get(
            "HTTP_USER_AGENT",
            "",
        ),
    )