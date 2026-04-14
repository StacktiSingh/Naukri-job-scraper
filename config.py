# config.py
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host":     os.environ.get("MYSQLHOST",     "localhost"),
    "user":     os.environ.get("MYSQLUSER",     "root"),
    "password": os.environ.get("MYSQLPASSWORD", "Monu#000"),
    "database": os.environ.get("MYSQLDATABASE", "naukri_jobs"),
    "port":     int(os.environ.get("MYSQLPORT",  "3306")),  # string default so int() never gets None
}

SCRAPE_URL = "https://www.naukri.com/development-jobs"
PAGES_TO_SCRAPE = 5