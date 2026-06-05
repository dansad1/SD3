from rest_framework.decorators import api_view
from rest_framework.response import Response

from backend.project.permissions.build_user_capabilities import build_user_capabilities


@api_view(["GET"])
def me(request):

    print("\n" + "=" * 60)
    print("🔥 /api/me/")
    print("=" * 60)

    user = request.user

    print("USER:", user)
    print("AUTH:", user.is_authenticated)

    if not user.is_authenticated:

        print("❌ NOT AUTHENTICATED")

        return Response({

            "authenticated": False,

            "user": None,

            "permissions": [],

            "capabilities": {},
        })

    print("PK:", user.pk)

    try:

        permissions = list(
            user.get_all_permissions()
        )

        print(
            f"✅ PERMISSIONS: {len(permissions)}"
        )

    except Exception as e:

        print("❌ PERMISSIONS ERROR")
        print(repr(e))

        raise

    try:

        capabilities = (
            build_user_capabilities(
                request
            )
        )

        response = {

            "authenticated": True,

            "user": {

                "id":
                    user.pk,

                "login":
                    getattr(
                        user,
                        "login",
                        None,
                    ),

                "username":
                    getattr(
                        user,
                        "username",
                        None,
                    ),

                "first_name":
                    getattr(
                        user,
                        "first_name",
                        None,
                    ),

                "last_name":
                    getattr(
                        user,
                        "last_name",
                        None,
                    ),
            },

            "permissions":
                permissions,

            "capabilities":
                capabilities,
        }

        print(
            "✅ RESPONSE BUILT"
        )

        print(
            "CAPABILITIES:"
        )

        print(
            capabilities
        )

        return Response(
            response
        )

    except Exception as e:

        print(
            "❌ RESPONSE BUILD ERROR"
        )

        print(
            repr(e)
        )

        raise