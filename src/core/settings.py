from pathlib import Path    

from pydantic_settings import BaseSettings, SettingsConfigDict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver


BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    
    input_file: Path = BASE_DIR / "input" / "requirements.txt"
    output_file: Path = BASE_DIR / "output" / "dependency_report.xlsx"

    snyk_package_url: str = (
            "https://security.snyk.io/package/pip/{package}"
        ) 

    pypi_api_url: str = (
            "https://pypi.org/pypi/{package}/json"
        )   


    webdriver_timeout: int = 15
    request_timeout: int = 15
    score_alert_limit: int = 65

    headless: bool = False    

    def create_chrome_options(self) -> Options:
        options = Options()
        
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        
        if self.headless:
                options.add_argument("--headless=new")
                options.add_argument("--window-size=1920,1080")
        
        return options        

    def create_driver(self) -> WebDriver:
            options = self.create_chrome_options()
            
            return webdriver.Chrome(options=options)
    
settings = Settings()    