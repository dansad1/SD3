from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, re_path
from django.views.decorators.csrf import ensure_csrf_cookie

from backend.engine.Resource.ResourceApi import resource_api
from backend.engine.action.ActionApi import (
    action_form_api,
    action_submit_api,
)
from backend.engine.form.FormApi import (
    entity_form_api,
    entity_form_submit_api,
)
from backend.engine.list.ListApi import (
    entity_filter_meta_api,
    entity_list_api,
    entity_list_meta_api,
    entity_list_settings_api,
)
from backend.engine.matrix.MatrixApi import (
    matrix_api,
    matrix_submit_api,
)
from backend.engine.utils.options_api import entity_options_api
from backend.engine.utils.upload_api import upload_api
from backend.generic.api.entity_export_api import entity_export_api
from backend.generic.api.entity_template_api import entity_template_api
from backend.project.audit.backup.download_view import (
    BackupDownloadView,
)
from backend.project.auth.me import me


@ensure_csrf_cookie
def csrf(request):
    return JsonResponse(
        {
            "status": "ok",
        }
    )


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),
    path(
        "api/csrf/",
        csrf,
        name="csrf",
    ),
    path(
        "api/me/",
        me,
        name="me",
    ),

    # =========================================================
    # ACTIONS
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
    # ENTITY LIST
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
    path(
        "api/entity/<str:entity>/filter/meta/",
        entity_filter_meta_api,
        name="entity-filter-meta",
    ),
    path(
        "api/entity/<str:entity>/export/",
        entity_export_api,
        name="entity-export",
    ),
    path(
        "api/entity/<str:entity>/template/",
        entity_template_api,
        name="entity-template",
    ),

    # =========================================================
    # ENTITY FORM
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
    # FILES
    # =========================================================

    path(
        "api/upload/",
        upload_api,
        name="upload",
    ),

    # =========================================================
    # MATRIX
    # =========================================================

    path(
        "api/matrix/<str:code>/",
        matrix_api,
        name="matrix",
    ),
    path(
        "api/matrix/<str:code>/submit/",
        matrix_submit_api,
        name="matrix-submit",
    ),

    # =========================================================
    # RESOURCE
    # =========================================================

    re_path(
        r"^api/resource/(?P<code>.+)/$",
        resource_api,
        name="resource",
    ),

    # =========================================================
    # BACKUP
    # =========================================================

    path(
        (
            "api/backup/"
            "<str:backup_id>/"
            "download/"
            "<str:filename>"
        ),
        BackupDownloadView.as_view(),
        name="backup-download",
    ),
]