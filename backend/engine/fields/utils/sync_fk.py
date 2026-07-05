def sync_fk(
    instance,
    field,
    value,
):
    if getattr(
        instance,
        field,
    ) != value:

        setattr(
            instance,
            field,
            value,
        )

        instance.save(
            update_fields=[
                field,
            ],
        )