from ..base import BaseImportExportService
from ..importer import EntityImporter

from .reader import ExcelReader
from .writer import ExcelWriter


class EntityExcelService(
    BaseImportExportService,
):

    def __init__(
        self,
        entity,
        request,
    ):
        super().__init__(
            entity,
            request,
        )

        self.reader = ExcelReader(
            max_rows=self.MAX_ROWS,
        )

        self.importer = EntityImporter(
            self,
        )

        self.writer = ExcelWriter(
            self,
        )

    # =====================================================
    # EXPORT
    # =====================================================

    def export(
        self,
        queryset,
    ):
        return self.writer.export(
            queryset,
        )

    def export_response(
        self,
    ):
        queryset = self.entity.get_queryset(
            self.request,
        )

        return self.writer.export_response(
            queryset,
        )

    # =====================================================
    # TEMPLATE
    # =====================================================

    def template(
        self,
    ):
        return self.writer.template()

    def template_response(
        self,
    ):
        return self.writer.template_response()

    # =====================================================
    # IMPORT
    # =====================================================

    def preview(
        self,
        file,
    ):
        data = self.reader.read(
            file,
        )

        return self.importer.preview(
            data["headers"],
            data["rows"],
        )

    parse = preview

    def commit(
        self,
        rows,
    ):
        return self.importer.commit(
            rows,
        )