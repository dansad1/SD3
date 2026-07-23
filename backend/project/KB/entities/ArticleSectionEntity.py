from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)
from backend.project.KB.models import (
    ArticleSection,
)
from backend.project.KB.services.ArticleSectionScopeService import (
    ArticleSectionScopeService,
)


class ArticleSectionEntity(BaseEntity):

    entity = "article-section"

    model = ArticleSection

    list_display = [
        "id",
        "name",
        "user_roles",
    ]

    search_fields = [
        "name",
    ]

    filter_fields = [
        "user_roles",
    ]

    ordering = [
        "name",
    ]

    capabilities = {
        "list": "knowledge.view",
        "view": "knowledge.view",
        "create": "knowledge.manage",
        "edit": "knowledge.manage",
        "delete": "knowledge.manage",
    }

    def get_prefetch_related(
        self,
    ):
        return [
            "user_roles",
        ]

    def apply_user_scope(
        self,
        request,
        qs,
    ):
        return (
            ArticleSectionScopeService
            .apply(
                request=request,
                queryset=qs,
            )
        )