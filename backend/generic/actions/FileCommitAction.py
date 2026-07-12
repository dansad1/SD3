from backend.engine.action.Base.BaseAction import BaseAction


class FileCommitAction(BaseAction):

    code = "files.commit"

    permission = None

    def run(
        self,
        request,
        payload,
        ctx,
    ):

        return {
            "status": "ok",
        }