from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)
from backend.project.KB.models import (
    Article,
)
from backend.project.KB.services.ArticleSchemaService import (
    ArticleSchemaService,
)
from backend.project.KB.services.ArticleValidationService import (
    ArticleValidationService,
)


class ArticleEntity(BaseEntity):

    model = Article
    entity = "article"

    list_display = [
        "id",
        "title",
        "section",
        "status",
        "updated_at",
    ]

    search_fields = [
        "title",
        "content",
    ]

    filter_fields = [
        "section",
        "status",
    ]

    exclude_fields = [
        "created_at",
        "updated_at",
    ]

    capabilities = {
        "list": "knowledge.view",
        "view": "knowledge.view",
        "create": "knowledge.manage",
        "edit": "knowledge.manage",
        "delete": "knowledge.manage",
    }

    def get_select_related(
        self,
    ):
        return [
            "section",
        ]

    def customize_field_schema(
        self,
        request,
        schema,
        field=None,
        obj=None,
    ):
        return (
            ArticleSchemaService
            .customize(
                request=request,
                schema=schema,
                article=obj,
            )
        )

    def validate(
        self,
        request,
        payload,
        instance=None,
    ):
        payload = super().validate(
            request=request,
            payload=payload,
            instance=instance,
        )

        return (
            ArticleValidationService
            .validate(
                payload=payload,
                instance=instance,
            )
        )