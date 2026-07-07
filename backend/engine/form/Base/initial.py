from backend.engine.fields.providers.registry import (
    relation_provider_registry,
)


def apply_query_initial(
    ctx,
):

    request = ctx.request

    query = (
        getattr(
            request,
            "query_params",
            None,
        )
        or request.GET
    )


    if ctx.mode != "create":
        return


    if ctx.data is None:
        ctx.data = {}


    field_names = {
        f["name"]
        for f in (
            ctx.fields
            or []
        )
    }


    result = {}


    # =====================================================
    # QUERY PARAMS
    # =====================================================

    for key, value in query.items():

        if key not in field_names:
            continue


        if value in (
            None,
            "",
        ):
            continue


        if (
            isinstance(
                value,
                str,
            )
            and value.isdigit()
        ):
            value = int(value)


        result[key] = value


    # =====================================================
    # RELATION PROVIDERS ONLY
    # =====================================================

    for field in (
        ctx.runtime_fields
        or []
    ):

        # query имеет приоритет
        if field.name in result:
            continue


        try:

            provider = (
                relation_provider_registry
                .get(
                    field.type,
                )
            )

        except RuntimeError:

            continue


        value = provider.get_initial(
            field,
            request=request,
            instance=ctx.instance,
        )


        if value is None:
            continue


        result[field.name] = (
            provider.serialize(
                field,
                value,
                request=request,
                instance=ctx.instance,
            )
        )


    # =====================================================
    # FINAL
    # =====================================================

    ctx.data = {
        **result,
        **(
            ctx.data
            or {}
        ),
    }


    print(
        "🔥 APPLY INITIAL:",
        result,
    )

    print(
        "🔥 FINAL ctx.data:",
        ctx.data,
    )