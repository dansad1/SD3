import pkgutil
import importlib
from django.apps import apps


def import_recursive(package):
    if not hasattr(package, "__path__"):
        return

    prefix = package.__name__ + "."

    for _, module_name, _ in pkgutil.walk_packages(
        package.__path__,
        prefix
    ):
        try:
            importlib.import_module(module_name)
            print("IMPORT:", module_name)
        except Exception as e:
            print("IMPORT ERROR:", module_name, e)


def autodiscover_all():

    # -------------------------
    # ENGINE
    # -------------------------

    try:
        import core.api.engine.action as action_pkg
        import_recursive(action_pkg)
    except ImportError:
        pass

    try:
        import core.api.engine.resource as resource_pkg
        import_recursive(resource_pkg)
    except ImportError:
        pass

    # -------------------------
    # PROJECT (твои модули)
    # -------------------------

    try:
        import core.api.Project as project_pkg
        import_recursive(project_pkg)
    except ImportError:
        pass

    # -------------------------
    # MATRIX (по apps)
    # -------------------------

    for app in apps.get_app_configs():
        try:
            matrix_pkg = importlib.import_module(
                f"{app.name}.api.matrix"
            )
            import_recursive(matrix_pkg)

        except ModuleNotFoundError:
            continue