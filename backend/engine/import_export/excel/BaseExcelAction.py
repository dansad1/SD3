from backend.engine.action.Base.BaseAction import BaseAction
from backend.engine.import_export.excel.EntityExcelService import EntityExcelService


class BaseExcelAction(BaseAction):

    entity_class = None

    def get_service(
        self,
        request,
    ):
        return EntityExcelService(
            self.entity_class(),
            request,
        )