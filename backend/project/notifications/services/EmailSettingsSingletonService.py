class EmailSettingsSingletonService:

    @classmethod
    def resolve_pk(
        cls,
        model,
        pk=None,
    ):
        if pk:
            return pk

        return (
            model.objects
            .order_by("id")
            .values_list(
                "pk",
                flat=True,
            )
            .first()
        )