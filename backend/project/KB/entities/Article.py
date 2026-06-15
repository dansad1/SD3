from django.db.models import Q

from backend.engine.entity.Base.BaseEntity import BaseEntity
from backend.project.KB.models import Article


class ArticleEntity(BaseEntity):

    entity = "article"

    model = Article

    capabilities = {
        "list": "knowledge.view",
        "view": "knowledge.view",
        "create": "knowledge.manage",
        "edit": "knowledge.manage",
        "delete": "knowledge.manage",
    }

    search_fields = [
        "code",
        "title",
        "content",
    ]
