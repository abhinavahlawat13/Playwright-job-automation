import sys
from config import Config
from utils.logger import logger
from utils.exporter import export_jobs_to_csv
from core.browser_manager import BrowserManager
from core.job_automation import JobAutomation

def main():
    logger.info("=== Starting Job Automation Pipeline ===")
    
    try:
        with BrowserManager.get_page() as page:
            bot = JobAutomation(page)
            
            # portal navigation
            bot.navigate_to_jobs()
            
            # search keyword
            bot.search_keyword(Config.SEARCH_KEYWORD)
            
            # extract job list
            jobs = bot.extract_jobs(limit=Config.MAX_RESULTS)
            
            # results
            if jobs:
                export_jobs_to_csv(jobs)
                logger.info(f"=== Successfully finished! Extracted {len(jobs)} jobs. ===")
            else:
                logger.warning("No listings found matching the keyword.")

    except Exception as e:
        logger.critical(f"Pipeline execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()