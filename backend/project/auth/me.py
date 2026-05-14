from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def me(request):

    print("\n" + "=" * 60)
    print("🔥 /api/me/")
    print("=" * 60)

    user = request.user

    print("USER:", user)
    print("AUTH:", user.is_authenticated)
    print("CLASS:", user.__class__)

    print("DIR USER:")
    print(dir(user))

    if not user.is_authenticated:

        print("❌ NOT AUTHENTICATED")

        return Response({
            "authenticated": False,
            "user": None,
            "permissions": [],
            "capabilities": {},
        })

    print("PK:", user.pk)

    print("USERNAME FIELD:")
    print(getattr(user, "USERNAME_FIELD", None))

    print("LOGIN:")
    print(getattr(user, "login", "NO LOGIN"))

    print("USERNAME:")
    print(getattr(user, "username", "NO USERNAME"))

    print("FIRST NAME:")
    print(getattr(user, "first_name", "NO FIRST NAME"))

    print("LAST NAME:")
    print(getattr(user, "last_name", "NO LAST NAME"))

    try:

        permissions = list(
            user.get_all_permissions()
        )

        print("✅ PERMISSIONS OK")

    except Exception as e:

        print("❌ PERMISSIONS ERROR")
        print(repr(e))

        raise

    try:

        response = {

            "authenticated": True,

            "user": {

                "id": user.pk,

                "login": getattr(
                    user,
                    "login",
                    None,
                ),

                "username": getattr(
                    user,
                    "username",
                    None,
                ),

                "first_name": getattr(
                    user,
                    "first_name",
                    None,
                ),

                "last_name": getattr(
                    user,
                    "last_name",
                    None,
                ),
            },

            "permissions": permissions,

            "capabilities": {},
        }

        print("✅ RESPONSE BUILT")
        print(response)

        return Response(response)

    except Exception as e:

        print("❌ RESPONSE BUILD ERROR")
        print(repr(e))

        raise