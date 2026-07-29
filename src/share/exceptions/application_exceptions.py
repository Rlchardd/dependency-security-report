
class ApplicationError(Exception):
    """Exceção-base para erros controlados pela aplicação."""


#Problema para encontrar ou abrir o arquivo.
class DependencyFileError(ApplicationError):
    """Erro ao acessar ou ler o arquivo de dependências."""

#Problema no conteúdo que foi lido.
class DependencyParseError(ApplicationError):
    """Erro ao interpretar uma dependência."""
    
class PyPiApiError(ApplicationError):
    """Erro durante a consulta à API do PyPI."""    

class PyPiPackageNotFoundError(PyPiApiError):
    """Pacote não encontrado no PyPI."""    
    
class SnykScrapingError(ApplicationError):
    """Erro durante a coleta de dados no portal Snyk."""    
    
class SnykPackageNotFoundError(SnykScrapingError):
    """Pacote não encontrado no portal Snyk."""    
    
class SpreadsheetError(ApplicationError):
    """Erro durante a geração da planilha Excel."""    