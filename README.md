# Dependency Security Report

Aplicação Python para analisar dependências declaradas em arquivos `requirements.txt` ou `pyproject.toml`, consultar informações públicas de segurança no portal Snyk, obter metadados pela API do PyPI e gerar um relatório consolidado em Excel.

## Objetivo

O projeto automatiza a análise de dependências Python por meio das seguintes etapas:

1. leitura das dependências do projeto;
2. consulta dos dados públicos de segurança no Snyk utilizando Selenium;
3. consulta de metadados dos pacotes por meio da API JSON do PyPI;
4. consolidação dos dados em modelos tipados;
5. geração de um relatório formatado em Excel;
6. destaque de pacotes cujo score de segurança esteja abaixo do limite configurado.

## Funcionalidades

- leitura de arquivos `requirements.txt`;
- leitura da seção `project.dependencies` de arquivos `pyproject.toml`;
- interpretação de nomes, versões e especificadores de dependências;
- automação do portal Snyk com Selenium;
- consulta à API pública do PyPI com Requests;
- geração de planilha com OpenPyXL;
- destaque visual para scores abaixo do limite definido;
- execução em ambientes de homologação e produção;
- logs estruturados durante todo o processamento;
- tratamento individual de falhas por pacote;
- encerramento seguro do navegador;
- arquitetura modular orientada a objetos.

## Tecnologias utilizadas

- Python 3.11
- Selenium
- Requests
- OpenPyXL
- Pydantic Settings
- Packaging
- uv
- Git e GitFlow

## Arquitetura

O projeto está organizado em camadas, separando regras de negócio, configurações e integrações externas.

```text
src/
├── application/
│   └── workflow.py
├── core/
│   ├── constants/
│   │   ├── environment_config.py
│   │   ├── hg.py
│   │   └── pd.py
│   ├── logger.py
│   └── settings.py
├── domain/
│   └── models/
│       ├── dependency_model.py
│       ├── package_report_model.py
│       ├── pypi_model.py
│       └── snyk_model.py
├── infrastructure/
│   ├── bots/
│   │   └── snyk_bot.py
│   ├── clients/
│   │   └── pypi_client.py
│   ├── readers/
│   │   ├── dependency_parser.py
│   │   ├── dependency_reader.py
│   │   ├── pyproject_reader.py
│   │   ├── reader_factory.py
│   │   └── requirements_reader.py
│   └── repositories/
│       └── excel_repository.py
└── share/
    └── exceptions/
        └── application_exceptions.py
```

### Responsabilidades das camadas

- `application`: coordena o fluxo principal da aplicação;
- `core`: centraliza configurações, ambientes e logs;
- `domain`: contém os modelos de dados da aplicação;
- `infrastructure`: implementa leitores, automações, clientes HTTP e geração do Excel;
- `share`: reúne exceções reutilizáveis.

## Fluxo de execução

```text
Arquivo de dependências
        ↓
ReaderFactory
        ↓
RequirementsReader ou PyProjectReader
        ↓
DependencyModel
        ↓
SnykBot + PyPiClient
        ↓
PackageReportModel
        ↓
ExcelRepository
        ↓
Relatório Excel
```

## Pré-requisitos

Antes de executar o projeto, é necessário ter instalado:

- Python 3.11 ou superior;
- Google Chrome;
- Git;
- uv.

Para verificar o Python:

```bash
python --version
```

Para verificar o uv:

```bash
uv --version
```

## Instalação

Clone o repositório:

```bash
git clone https://github.com/R1chardd/dependency-security-report.git
```

Entre na pasta do projeto:

```bash
cd dependency-security-report
```

Instale as dependências e crie o ambiente virtual:

```bash
uv sync
```

## Configuração

Crie um arquivo `.env` a partir do `.env.example`.

No PowerShell:

```powershell
Copy-Item .env.example .env
```

No Linux ou macOS:

```bash
cp .env.example .env
```

Exemplo de configuração:

```env
# hg = homologação
# pd = produção
ENVIRONMENT=hg

# Arquivo que contém as dependências analisadas
INPUT_FILE=input/requirements.txt

# Tempo máximo de espera do Selenium
WEBDRIVER_TIMEOUT=15

# Tempo máximo das requisições HTTP
REQUEST_TIMEOUT=15

# Scores abaixo deste valor serão destacados
SCORE_ALERT_LIMIT=65
```

## Ambientes

A aplicação possui dois perfis de execução.

| Ambiente | Código | Navegador | Log | Relatório |
|---|---|---|---|---|
| Homologação | `hg` | Visível | `DEBUG` | `dependency_report_hg.xlsx` |
| Produção | `pd` | Headless | `INFO` | `dependency_report.xlsx` |

### Homologação

```env
ENVIRONMENT=hg
```

Nesse ambiente, o Chrome fica visível para facilitar testes, acompanhamento e depuração da automação.

### Produção

```env
ENVIRONMENT=pd
```

Nesse ambiente, o Chrome é executado em modo headless, sem abrir uma janela na tela.

## Arquivos de entrada

A aplicação aceita dois formatos.

### requirements.txt

Exemplo:

```text
requests==2.34.2
selenium>=4.36.0
openpyxl
pydantic-settings>=2.14.2
```

### pyproject.toml

Exemplo:

```toml
[project]
dependencies = [
    "requests>=2.34.2",
    "selenium>=4.36.0",
    "openpyxl>=3.1.5",
]
```

O caminho do arquivo analisado deve ser informado no `.env`:

```env
INPUT_FILE=input/requirements.txt
```

ou:

```env
INPUT_FILE=input/pyproject.toml
```

## Execução

Execute a aplicação pela raiz do projeto:

```bash
uv run python main.py
```

Durante a execução, o sistema:

1. identifica o tipo do arquivo de entrada;
2. lê e interpreta as dependências;
3. acessa o portal público do Snyk;
4. consulta a API JSON do PyPI;
5. consolida as informações;
6. gera o relatório na pasta `output`.

## Relatório gerado

O relatório reúne informações como:

- nome do pacote;
- versão declarada;
- score de segurança do Snyk;
- quantidade ou situação das vulnerabilidades encontradas;
- versão mais recente publicada no PyPI;
- descrição do pacote;
- licença;
- data da publicação mais recente.

A planilha também possui:

- cabeçalhos formatados;
- filtro automático;
- primeira linha congelada;
- largura das colunas ajustada;
- formatação de datas;
- destaque visual de pacotes com score abaixo do limite.

## Regra de destaque do score

O limite padrão é:

```env
SCORE_ALERT_LIMIT=65
```

Somente scores estritamente menores que o limite são destacados.

Exemplo:

```text
Score 64 → destacado
Score 65 → não destacado
Score 66 → não destacado
```

O limite pode ser alterado pelo arquivo `.env`.

## Tratamento de erros

A aplicação possui tratamento para situações como:

- arquivo de entrada não encontrado;
- formato de arquivo não suportado;
- dependência inválida;
- pacote não encontrado no PyPI;
- falha de conexão com serviços externos;
- elementos do Snyk não encontrados;
- tempo limite do Selenium;
- planilha aberta durante a tentativa de gravação;
- erros inesperados durante o processamento.

Uma falha em determinado pacote é registrada nos logs sem necessariamente interromper a análise das demais dependências.

O navegador é encerrado ao final da execução, inclusive quando ocorre uma exceção.

## Variáveis de ambiente

| Variável | Descrição | Valor padrão |
|---|---|---|
| `ENVIRONMENT` | Ambiente de execução | `hg` |
| `INPUT_FILE` | Arquivo de dependências | `input/requirements.txt` |
| `WEBDRIVER_TIMEOUT` | Tempo máximo do Selenium | `15` |
| `REQUEST_TIMEOUT` | Tempo máximo das requisições | `15` |
| `SCORE_ALERT_LIMIT` | Limite de alerta do score | `65` |

## Observações

- A execução depende de conexão com a internet.
- O Google Chrome deve estar instalado.
- Os dados do Snyk são coletados de páginas públicas utilizando Selenium.
- Alterações na estrutura visual do portal Snyk podem exigir atualização dos seletores.
- Alguns pacotes podem não disponibilizar licença, descrição ou histórico completo no PyPI.
- Os relatórios da pasta `output` são gerados localmente e não são versionados pelo Git.

## Validação realizada

A aplicação foi validada manualmente nos dois ambientes:

- homologação, com Chrome visível;
- produção, com Chrome em modo headless;
- leitura de `requirements.txt`;
- leitura de `pyproject.toml`;
- consulta ao Snyk;
- consulta ao PyPI;
- geração e formatação do relatório Excel.

## Autor

Desenvolvido por **Richard Shayron Fernandes Lobo**.

GitHub: `@R1chardd`