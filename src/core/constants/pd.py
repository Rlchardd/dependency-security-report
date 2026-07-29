from .environment_config import EnvironmentConfig

constants = EnvironmentConfig(

    name="production",

    headless=True,

    log_level="INFO",

    output_filename="dependency_report.xlsx",
)