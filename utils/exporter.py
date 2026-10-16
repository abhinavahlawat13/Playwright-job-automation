import csv
from typing import List, Dict, Any
from config import Config
from utils.logger import logger

def export_jobs_to_csv(jobs: List[Dict[str, Any]], filename: str = "jobs.csv") -> str:
    if not jobs:
        logger.warning("No job records provided for export.")
        return ""

    filepath = Config.OUTPUT_DIR / filename
    fieldnames = ["title", "company", "location", "url"]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(jobs)

    logger.info(f"Export complete: {len(jobs)} records written to {filepath.name}")
    return str(filepath)