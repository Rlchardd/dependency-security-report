from datetime import datetime
import requests
from src.domain.models import (
    DependencyModel,
    PyPiModel,
)
from src.share.exceptions import (
    PyPiApiError,
    PyPiPackageNotFoundError,
)

class PyPiClient:

    def __init__(
        self,
        api_url: str,
        timeout: int,
    ) -> None:


        self.api_url = api_url


        self.timeout = timeout


    def get_package(
        self,
        dependency: DependencyModel,
    ) -> PyPiModel:


        url = self.api_url.format(
            package=dependency.name
        )

        try:


            response = requests.get(
                url,
                timeout=self.timeout,
            )


        except requests.Timeout as error:
            raise PyPiApiError(
                "Tempo limite excedido ao consultar o pacote "
                f"{dependency.name!r} no PyPI."
            ) from error


        except requests.ConnectionError as error:
            raise PyPiApiError(
                "Não foi possível estabelecer conexão com o PyPI "
                f"para consultar {dependency.name!r}."
            ) from error


        except requests.RequestException as error:
            raise PyPiApiError(
                "Falha inesperada durante a consulta ao PyPI "
                f"para o pacote {dependency.name!r}."
            ) from error


        if response.status_code == 404:
            raise PyPiPackageNotFoundError(
                f"Pacote não encontrado no PyPI: "
                f"{dependency.name!r}."
            )


        try:
            response.raise_for_status()


        except requests.HTTPError as error:
            raise PyPiApiError(
                "O PyPI respondeu com erro ao consultar "
                f"{dependency.name!r}. "
                f"Status HTTP: {response.status_code}."
            ) from error


        try:
            data = response.json()


        except requests.JSONDecodeError as error:
            raise PyPiApiError(
                "O PyPI retornou uma resposta JSON inválida "
                f"para {dependency.name!r}."
            ) from error


        if not isinstance(data, dict):
            raise PyPiApiError(
                "A resposta do PyPI possui um formato inesperado "
                f"para {dependency.name!r}."
            )


        info = data.get("info")


        if not isinstance(info, dict):
            raise PyPiApiError(
                "Os metadados do pacote não foram encontrados "
                f"na resposta do PyPI: {dependency.name!r}."
            )


        urls = data.get("urls", [])


        if not isinstance(urls, list):
            urls = []


        license_name = self._extract_license(info)


        last_publication = self._extract_last_publication(
            urls
        )


        return PyPiModel(

            name=self._optional_text(
                info.get("name")
            ) or dependency.name,


            description=self._optional_text(
                info.get("summary")
            ),


            license=license_name,


            latest_version=self._optional_text(
                info.get("version")
            ),


            last_publication=last_publication,
        )


    @staticmethod
    def _extract_license(
        info: dict,
    ) -> str | None:


        license_expression = PyPiClient._optional_text(
            info.get("license_expression")
        )


        if license_expression:
            return license_expression


        return PyPiClient._optional_text(
            info.get("license")
        )


    @staticmethod
    def _extract_last_publication(
        urls: list,
    ) -> datetime | None:


        publication_dates: list[datetime] = []


        for file_data in urls:


            if not isinstance(file_data, dict):
                continue


            raw_date = (
                file_data.get("upload_time_iso_8601")
                or file_data.get("upload_time")
            )

            if not isinstance(raw_date, str):
                continue


            normalized_date = raw_date.replace(
                "Z",
                "+00:00",
            )

            try:

                publication_date = datetime.fromisoformat(
                    normalized_date
                )


            except ValueError:
                continue


            publication_dates.append(
                publication_date
            )


        if not publication_dates:
            return None


        return max(publication_dates)


    @staticmethod
    def _optional_text(
        value: object,
    ) -> str | None:


        if value is None:
            return None


        text = str(value).strip()


        if text:
            return text


        return None