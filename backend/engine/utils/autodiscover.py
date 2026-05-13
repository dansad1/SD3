# backend/engine/utils/autodiscover.py

import importlib
import pkgutil

import backend


# =========================================================
# SKIP
# =========================================================

SKIP_PARTS = {
    "migrations",
    "__pycache__",
    "tests",
    "node_modules",
    "static",
    "media",
    "asgi",
    "wsgi",
    "settings",
}


# =========================================================
# HELPERS
# =========================================================

def should_skip(module_name):

    parts = module_name.split(".")

    return any(
        part in SKIP_PARTS
        for part in parts
    )


# =========================================================
# AUTODISCOVER
# =========================================================

def autodiscover_all():

    print()
    print("📦 AUTODISCOVER START")
    print()

    imported = 0
    errors = 0

    for _, module_name, _ in pkgutil.walk_packages(
        backend.__path__,
        backend.__name__ + ".",
    ):

        # =========================================
        # SKIP
        # =========================================

        if should_skip(module_name):
            continue

        # =========================================
        # IMPORT
        # =========================================

        try:

            importlib.import_module(module_name)

            imported += 1

        except Exception as e:

            errors += 1

            print()
            print("❌ IMPORT ERROR")
            print("MODULE:", module_name)
            print("ERROR :", str(e))
            print()

    # =========================================
    # SUMMARY
    # =========================================

    print()
    print("╔══════════════════════════════════════╗")
    print("║         AUTODISCOVER DONE           ║")
    print("╚══════════════════════════════════════╝")

    print(
        f"📦 IMPORTED: {imported}"
    )

    print(
        f"❌ ERRORS:   {errors}"
    )

    print()