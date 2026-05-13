from backend.engine.Resource.ResourceRegistry import resource_registry
from backend.engine.action.ActionRegistry import actions
from backend.engine.entity.EntityRegistry import entity_registry
from backend.engine.form.FormRegistry import form_registry
from backend.engine.list.ListRegistry import list_registry
from backend.engine.matrix.MatrixRegistry import matrix_registry
from backend.engine.utils.autodiscover import autodiscover_all


REGISTRIES = [
    ("ENTITY", entity_registry),
    ("ACTION", actions),
    ("RESOURCE", resource_registry),
    ("MATRIX", matrix_registry),
    ("FORM", form_registry),
    ("LIST", list_registry),
]


def bootstrap(force=True):

    # ====================================
    # SNAPSHOT BEFORE
    # ====================================

    before = {
        name: set(
            registry.storage.by_code.keys()
        )
        for name, registry in REGISTRIES
    }

    # ====================================
    # CLEAR
    # ====================================

    if force:

        for _, registry in REGISTRIES:
            registry.clear()

    # ====================================
    # IMPORTS
    # ====================================

    autodiscover_all()

    # ====================================
    # DISCOVER
    # ====================================

    for _, registry in REGISTRIES:
        registry.autodiscover(force=force)

    # ====================================
    # DIFF
    # ====================================

    print()
    print("╔══════════════════════════════════════╗")
    print("║         REGISTRY BOOTSTRAP          ║")
    print("╚══════════════════════════════════════╝")

    for name, registry in REGISTRIES:

        after = set(
            registry.storage.by_code.keys()
        )

        added = sorted(
            after - before[name]
        )

        removed = sorted(
            before[name] - after
        )

        total = len(after)

        # ====================================
        # ICON
        # ====================================

        icon = "✅"

        if added:
            icon = "🟢"

        elif removed:
            icon = "🔴"

        # ====================================
        # SUMMARY
        # ====================================

        print()
        print(
            f"{icon} "
            f"{name:<10} "
            f"total={total:<3} "
            f"added={len(added):<3} "
            f"removed={len(removed):<3}"
        )

        # ====================================
        # DETAILS
        # ====================================

        for code in added:
            print(f"   + {code}")

        for code in removed:
            print(f"   - {code}")

    print()