import importlib
import pkgutil

from django.core.exceptions import ImproperlyConfigured


DISCOVERY_ROOTS = [
    "backend.project",
    "backend.generic",
]

SKIP_PARTS = {
    "migrations",
    "__pycache__",
    "tests",
    "management",
    "node_modules",
    "static",
    "media",
    "templates",
    "settings",
    "urls",
    "asgi",
    "wsgi",
}


_discovered = False


def should_skip(module_name):
    parts = module_name.split(".")

    return any(
        part in SKIP_PARTS
        for part in parts
    )


def autodiscover_all(force=False):
    global _discovered

    if _discovered and not force:
        return {
            "imported": 0,
            "errors": [],
            "skipped": True,
        }

    print()
    print("📦 AUTODISCOVER START")
    print()

    imported = 0
    errors = []

    for root_name in DISCOVERY_ROOTS:
        root_module = importlib.import_module(
            root_name
        )

        module_path = getattr(
            root_module,
            "__path__",
            None,
        )

        if module_path is None:
            continue

        for _, module_name, _ in pkgutil.walk_packages(
            module_path,
            root_name + ".",
        ):
            if should_skip(module_name):
                continue

            try:
                importlib.import_module(
                    module_name
                )
                imported += 1

            except Exception as exc:
                errors.append(
                    {
                        "module": module_name,
                        "error": repr(exc),
                    }
                )

                print()
                print("❌ IMPORT ERROR")
                print("MODULE:", module_name)
                print("ERROR :", repr(exc))
                print()

    print()
    print("╔══════════════════════════════════════╗")
    print("║         AUTODISCOVER DONE           ║")
    print("╚══════════════════════════════════════╝")
    print(f"📦 IMPORTED: {imported}")
    print(f"❌ ERRORS:   {len(errors)}")
    print()

    if errors:
        failed_modules = ", ".join(
            item["module"]
            for item in errors
        )

        raise ImproperlyConfigured(
            "Autodiscover завершён с ошибками: "
            f"{failed_modules}"
        )

    _discovered = True

    return {
        "imported": imported,
        "errors": [],
        "skipped": False,
    }