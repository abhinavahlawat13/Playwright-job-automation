# Playwright Job Search Automation

A Python script that uses Microsoft Playwright to search for listings on `python.org/jobs`, logs each step, captures proof screenshots, and saves the extracted job details to a CSV file.

---

## Features

- **Automated Search:** Navigates to `python.org/jobs` and inputs search queries into the form.
- **Configurable:** Settings like search keywords, result limits, and headless mode are managed via a `.env` file.
- **Step Screenshots:** Captures screenshots at navigation, form input, and data extraction stages.
- **Structured Logging:** Tracks execution flow and errors in both the terminal and daily log files.
- **CSV Export:** Saves scraped listings (Job Title, Category/Type, Location, URL) to `output/jobs.csv`.
- **Clean Browser Lifecycle:** Uses context managers to ensure the browser closes properly even if an error occurs.

---

## Project Structure

```text
Playwright-Job-automation/
├── core/
│   ├── __init__.py
│   ├── browser_manager.py     # Browser launch and shutdown logic
│   └── job_automation.py      # Page navigation, form input, and job extraction
├── utils/
│   ├── __init__.py
│   ├── exporter.py            # CSV file creation
│   └── logger.py              # Terminal and file logger setup
├── config.py                  # Loads settings from .env
├── main.py                    # Script entry point
├── requirements.txt