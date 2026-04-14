# database/db.py

import mysql.connector
from config import DB_CONFIG

def get_connection(use_db=True):
    config = DB_CONFIG.copy()
    if not use_db:
        config.pop("database")  # connect without DB first
    return mysql.connector.connect(**config)

def create_table():
    conn = get_connection(use_db=False)  # no DB yet
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS naukri_jobs")
    cursor.execute("USE naukri_jobs")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            company VARCHAR(255),
            location VARCHAR(255),
            experience VARCHAR(100),
            salary VARCHAR(100),
            skills TEXT,
            posted_date VARCHAR(100),
            job_url TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY unique_job (title(100), company(100))
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("Database and table ready.")

def insert_jobs(jobs: list[dict]):
    conn = get_connection(use_db=True)  # DB exists now
    cursor = conn.cursor()
    inserted = 0
    skipped = 0
    for job in jobs:
        try:
            cursor.execute("""
                INSERT IGNORE INTO jobs 
                (title, company, location, experience, salary, skills, posted_date, job_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                job.get("title"),
                job.get("company"),
                job.get("location"),
                job.get("experience"),
                job.get("salary"),
                job.get("skills"),
                job.get("posted_date"),
                job.get("job_url")
            ))
            if cursor.rowcount > 0:
                inserted += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"Insert error: {e}")
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Inserted: {inserted} | Skipped (duplicates): {skipped}")