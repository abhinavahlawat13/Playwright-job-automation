import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

class Config:
    HEADLESS: bool = os.getenv("HEADLESS", "false").lower() == "true"
    SEARCH_KEYWORD: str = os.getenv("SEARCH_KEYWORD", "python")
    MAX_RESULTS: int = int(os.getenv("MAX_RESULTS", "5"))
    BASE_URL: str = "https://weworkremotely.com"

    # Paths
    OUTPUT_DIR: Path = BASE_DIR / "output"
    LOG_DIR: Path = BASE_DIR / "logs"
    SCREENSHOT_DIR: Path = BASE_DIR / "screenshots"

    @classmethod
    def setup_dirs(cls):
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        cls.LOG_DIR.mkdir(parents=True, exist_ok=True)
        cls.SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

Config.setup_dirs()