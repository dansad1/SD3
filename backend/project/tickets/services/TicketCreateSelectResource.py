from backend.engine.Resource.BaseResource import (
    BaseResource,
)
from backend.engine.entity.EntityRegistry import (
    entity_registry,
)


class TicketCreateSelectResource(
    BaseResource,
):

    code = "ticket.create.select"

    def get(
        self,
        request,
        **kwargs,
    ):

        service_entity = entity_registry.get(
            "service",
        )

        services = []

        queryset = (
            service_entity
            .get_queryset(request)
            .filter(
                archived=False,
            )
        )

        for service in queryset:

            types = []

            for ticket_type in (
                service.ticket_types
                .all()
                .order_by("name")
            ):

                types.append({

                    "id":
                        ticket_type.pk,

                    "title":
                        ticket_type.name,

                    "description":
                        "",

                    "service":
                        service.pk,

                    "type":
                        ticket_type.pk,

                })

            if not types:
                continue

            services.append({

                "id":
                    service.pk,

                "title":
                    service.get_full_path(),

                "description":
                    service.description,

                "types":
                    types,

            })

        return {

            "title":
                "Создание заявки",

            "description":
                "Выберите сервис и тип обращения",

            "services":
                services,

        }