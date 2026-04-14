# config.py
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host":     os.environ.get("MYSQLHOST"),
    "user":     os.environ.get("MYSQLUSER"),
    "password": os.environ.get("MYSQLPASSWORD"),
    "database": os.environ.get("MYSQLDATABASE"),
    "port":     int(os.environ.get("MYSQLPORT")),
}

SCRAPE_URL = "https://www.naukri.com/development-jobs"
PAGES_TO_SCRAPE = 5