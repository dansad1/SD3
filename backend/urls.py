
from django.contrib import admin
from django.urls import path, re_path

from backend.engine.Resource.ResourceApi import resource_api
from backend.engine.action.ActionApi import action_submit_api, action_form_api
from backend.engine.form.FormApi import entity_form_submit_api, entity_form_api
from backend.engine.list.ListApi import entity_list_api, entity_list_settings_api, entity_list_meta_api
from backend.engine.matrix.MatrixApi import matrix_submit_api, matrix_api
from backend.engine.utils.options_api import entity_options_api
from backend.engine.utils.upload_api import upload_api
from backend.project.auth.me import me

urlpatterns = [
    path("api/me/", me),
    # =========================================================
    # ⚡ ACTIONS (DSL, supports dots)
    # =========================================================

    re_path(
        r"^api/action/(?P<code>.+)/form/$",
        action_form_api,
        name="action-form",
    ),
    re_path(
        r"^api/action/(?P<code>.+)/submit/$",
        action_submit_api,
        name="action-submit",
    ),

    # =========================================================
    # 📊 ENTITY LIST
    # =========================================================

    path(
        "api/entity/<str:entity>/list/",
        entity_list_api,
        name="entity-list",
    ),
    path(
        "api/entity/<str:entity>/meta/",
        entity_list_meta_api,
        name="entity-meta",
    ),
    path(
        "api/entity/<str:entity>/settings/",
        entity_list_settings_api,
        name="entity-settings",
    ),
    path(
        "api/entity/<str:entity>/options/",
        entity_options_api,
        name="entity-options",
    ),

    # =========================================================
    # 📝 ENTITY FORM (CRUD)
    # =========================================================

    path(
        "api/entity/<str:entity>/form/",
        entity_form_api,
        name="entity-form",
    ),
    path(
        "api/entity/<str:entity>/form/submit/",
        entity_form_submit_api,
        name="entity-submit",
    ),

    # =========================================================
    # 📎 FILES
    # =========================================================

    path(
        "api/upload/",
        upload_api,
        name="upload",
    ),

    # =========================================================
    # 🧮 MATRIX (supports dots)
    # =========================================================
path("api/matrix/<str:code>/", matrix_api),
path("api/matrix/<str:code>/submit/", matrix_submit_api),
    # =========================================================
    # 🌐 RESOURCE (supports dots + :)
    # =========================================================

    re_path(
        r"^api/resource/(?P<code>.+)/$",
        resource_api,
        name="resource",
    ),
]
