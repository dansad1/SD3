# =====================================================
# backend/engine/list/Base/filters.py
# =====================================================

def apply_filters(ctx):

    entity = ctx.entity


    runtime_fields = (

        entity.get_fields(

            ctx.request

        )

    )


    field_map = {

        field.name: field

        for field in runtime_fields

    }


    excluded = set(

        getattr(

            entity,

            "filter_exclude_fields",

            [],

        )

        or []

    )


    reserved = {

        "page",

        "page_size",

        "sort",

        "search",

        "q",

    }


    qs = ctx.qs


    for key in ctx.request.GET:


        if key in reserved:
            continue


        field = field_map.get(

            key

        )


        if not field:
            continue


        if field.name in excluded:
            continue


        values = (

            ctx.request.GET.getlist(

                key

            )

        )


        value = (

            values

            if len(values) > 1

            else values[0]

        )


        print(

            "FILTER",

            field.name,

            value,

        )


        qs = field.apply_filter(

            qs,

            value,

        )


    ctx.qs = qs