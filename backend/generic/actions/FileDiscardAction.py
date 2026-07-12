from backend.engine.action.Base.BaseAction import BaseAction
from backend.generic.models import StoredFile


class FileDiscardAction(BaseAction):

    code = "files.discard"

    permission = None

    def run(
        self,
        request,
        payload,
        ctx,
    ):

        ids = payload.get(
            "ids",
            [],
        )

        StoredFile.objects.filter(
            pk__in=ids,
        ).delete()

        return {
            "status": "ok",
        }