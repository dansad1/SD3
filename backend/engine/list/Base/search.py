from django.db.models import Q


def apply_search(ctx):

    value = (
        ctx.request.GET.get("search")
        or ctx.request.GET.get("q")
        or ""
    ).strip()

    if not value:
        return

    allowed = set(
        ctx.entity.search_fields
        or []
    )

    query = Q()

    for field in (
        ctx.runtime_fields
        or []
    ):

        if field.name not in allowed:
            continue

        if not field.field_type.searchable:
            continue

        q = field.build_search_q(value)

        print(field.name, q)

        query |= q

    print(query)

    if query.children:

        ctx.qs = (
            ctx.qs
            .filter(query)
            .distinct()
        )

        print(ctx.qs.query)