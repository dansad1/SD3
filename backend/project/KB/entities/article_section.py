from backend.engine.entity.Base.BaseEntity import BaseEntity
from backend.project.KB.models import ArticleSection


class ArticleSectionEntity(BaseEntity):

    entity = "article-section"

    model = ArticleSection

    capabilities = {
        "list": "knowledge.view",
        "view": "knowledge.view",
        "create": "knowledge.manage",
        "edit": "knowledge.manage",
        "delete": "knowledge.manage",
    }