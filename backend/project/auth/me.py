from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def me(request):

    user = request.user

    if not user.is_authenticated:
        return Response({
            "authenticated": False,
            "user": None,
            "permissions": [],
            "capabilities": {},
        })

    permissions = list(
        user.get_all_permissions()
    )

    return Response({
        "authenticated": True,

        "user": {
            "id": user.pk,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
        },

        "permissions": permissions,

        # future:
        # entity/action/matrix capabilities
        "capabilities": {},
    })