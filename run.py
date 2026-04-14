# run.py  — test the full pipeline manually before adding scheduler

from database.db import create_table, insert_jobs
from scraper.job_scraper import run_scraper
from data.cleaner import clean_jobs

if __name__ == "__main__":
    print("=== Step 1: Creating table ===")
    create_table()

    print("\n=== Step 2: Scraping ===")
    raw_jobs = run_scraper()

    print("\n=== Step 3: Cleaning ===")
    clean = clean_jobs(raw_jobs)

    print("\n=== Step 4: Inserting into DB ===")
    insert_jobs(clean)

    print("\nDone! Check your MySQL database.")