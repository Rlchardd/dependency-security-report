from datetime import datetime, timezone
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import (
    Alignment,
    Font,
    PatternFill,
)
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet
from src.domain.models import PackageReportModel
from src.share.exceptions import SpreadsheetError
class ExcelRepository:

    HEADERS: tuple[str, ...] = (
        "Dependência",
        "Versão no projeto",
        "Última versão",
        "Descrição",
        "Score",
        "Vulnerabilidades",
        "Licença",
        "Última publicação",
    )
    def __init__(
        self,
        output_file: Path,
        score_alert_limit: int,
    ) -> None:

        self.output_file = output_file
        self.score_alert_limit = score_alert_limit

        self.workbook = Workbook()


        self.worksheet: Worksheet = self.workbook.active

        self.worksheet.title = "Dependências"

        self._create_header()

    def _create_header(self) -> None:

        self.worksheet.append(
            list(self.HEADERS)
        )

        for cell in self.worksheet[1]:

            cell.font = Font(
                bold=True,
                color="FFFFFF",
            )

            cell.fill = PatternFill(
                fill_type="solid",
                fgColor="1F4E78",
            )


            cell.alignment = Alignment(
                horizontal="center",
                vertical="center",
            )


        self.worksheet.row_dimensions[1].height = 24

        self.worksheet.freeze_panes = "A2"


    def add(
        self,
        report: PackageReportModel,
    ) -> None:


        publication_date = self._prepare_datetime(
            report.last_publication
        )


        row = [
            report.name,
            report.project_version or "Não informada",
            report.latest_version or "Não informada",
            report.description or "Não informada",
            report.score,
            report.vulnerabilities,
            report.license or "Não informada",
            publication_date or "Não informada",
        ]


        self.worksheet.append(row)


        current_row = self.worksheet.max_row

        publication_cell = self.worksheet.cell(
            row=current_row,
            column=8,
        )


        if isinstance(
            publication_cell.value,
            datetime,
        ):
            publication_cell.number_format = (
                "dd/mm/yyyy hh:mm"
            )


        for column_number in (
            2,
            3,
            5,
            6,
            8,
        ):
            self.worksheet.cell(
                row=current_row,
                column=column_number,
            ).alignment = Alignment(
                horizontal="center",
                vertical="center",
            )


        self.worksheet.cell(
            row=current_row,
            column=4,
        ).alignment = Alignment(
            vertical="top",
            wrap_text=True,
        )


        if (
            report.score is not None
            and report.score
            < self.score_alert_limit
        ):

            self._highlight_alert_row(
                row_number=current_row
            )


    def _highlight_alert_row(
        self,
        row_number: int,
    ) -> None:


        alert_fill = PatternFill(
            fill_type="solid",
            fgColor="FFC7CE",
        )


        alert_font = Font(
            color="9C0006",
        )


        for cell in self.worksheet[row_number]:


            cell.fill = alert_fill


            cell.font = alert_font


        score_cell = self.worksheet.cell(
            row=row_number,
            column=5,
        )


        score_cell.font = Font(
            bold=True,
            color="9C0006",
        )

    @staticmethod
    def _prepare_datetime(
        value: datetime | None,
    ) -> datetime | None:

        if value is None:
            return None

        if value.tzinfo is not None:


            return value.astimezone(
                timezone.utc
            ).replace(
                tzinfo=None
            )


        return value


    def _adjust_column_widths(self) -> None:


        for column_cells in self.worksheet.columns:


            maximum_length = 0


            column_letter = get_column_letter(
                column_cells[0].column
            )


            for cell in column_cells:


                if cell.value is None:
                    cell_text = ""
                else:

                    cell_text = str(cell.value)


                maximum_length = max(
                    maximum_length,
                    len(cell_text),
                )


            adjusted_width = maximum_length + 2


            adjusted_width = max(
                adjusted_width,
                12,
            )


            adjusted_width = min(
                adjusted_width,
                60,
            )


            self.worksheet.column_dimensions[
                column_letter
            ].width = adjusted_width


    def save(self) -> None:


        self.output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )


        self._adjust_column_widths()


        self.worksheet.auto_filter.ref = (
            self.worksheet.dimensions
        )

        try:

            self.workbook.save(
                self.output_file
            )


        except PermissionError as error:
            raise SpreadsheetError(
                "Não foi possível salvar a planilha. "
                "Verifique se o arquivo está aberto no Excel: "
                f"{self.output_file}"
            ) from error


        except OSError as error:
            raise SpreadsheetError(
                "Ocorreu um erro ao salvar a planilha em: "
                f"{self.output_file}"
            ) from error