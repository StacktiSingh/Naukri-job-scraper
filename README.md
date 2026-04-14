# Naukri Job Intelligence Dashboard

A fully automated web scraping and analytics pipeline that collects Python job listings from Naukri.com, stores them in MySQL, and presents live insights through a Flask dashboard — updated every 6 hours automatically.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey?style=flat-square&logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?style=flat-square&logo=mysql)
![Railway](https://img.shields.io/badge/Deployed-Railway-blueviolet?style=flat-square)

---

## What it does

- Scrapes live job listings from Naukri.com (title, company, location, salary, experience, skills)
- Cleans and deduplicates data using Pandas before storing
- Stores all records in a MySQL database with timestamps
- Serves a dark-themed Flask dashboard with charts, filters, and paginated job cards
- Runs automatically every 6 hours via APScheduler — zero manual work after setup

---

## Tech stack

| Layer | Technology |
|---|---|
| Scraping | Python, Requests, BeautifulSoup4 |
| Data cleaning | Pandas, NumPy |
| Database | MySQL 8.0 |
| Backend | Flask, mysql-connector-python |
| Frontend | HTML, CSS, JavaScript, Chart.js |
| Scheduling | APScheduler |
| Deployment | Railway |

---

## Project structure

```
naukri-job-scraper/
├── scraper/
│   └── naukri_scraper.py      # Scrapes job listings from Naukri
├── data/
│   └── cleaner.py             # Cleans raw data with Pandas
├── database/
│   └── db.py                  # MySQL connection, table creation, inserts
├── dashboard/
│   ├── app.py                 # Flask app and API routes
│   └── templates/
│       └── index.html         # Dashboard UI
├── run.py                     # Manual one-time pipeline trigger
├── config.py                  # DB config via environment variables
├── Procfile                   # Railway/Render start command
├── runtime.txt                # Python version
├── requirements.txt           # All dependencies
└── .env                       # Local environment variables (not committed)
```

---

## Getting started locally

### 1. Clone the repo

```bash
git clone https://github.com/StacktiSingh/naukri-job-scraper.git
cd naukri-job-scraper
```

### 2. Create and activate virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```
MYSQLHOST=localhost
MYSQLUSER=root
MYSQLPASSWORD=your_password
MYSQLDATABASE=naukri_jobs
MYSQLPORT=3306

SCRAPE_URL=https://www.naukri.com/python-jobs
PAGES_TO_SCRAPE=5
```

### 5. Run the pipeline (first time)

```bash
python run.py
```

This creates the database, scrapes Naukri, cleans the data, and inserts records.

### 6. Start the dashboard

```bash
python dashboard/app.py
```

Open `http://127.0.0.1:8000` in your browser.

### 7. Start the scheduler (auto-scrape every 6 hours)

```bash
python scheduler.py
```

Keep this terminal open. Press `Ctrl+C` to stop.

---

## Dashboard features

- **Stats bar** — total jobs, unique companies, locations, and jobs with salary data
- **Top companies chart** — bar chart of most active hiring companies
- **Location distribution** — doughnut chart of jobs by city
- **Skills heatmap** — most demanded skills with counts
- **Job cards** — paginated grid with title, company, location, salary, experience, and skills
- **Search** — filter by title, company, or skill in real time
- **Location filter** — dropdown to filter by city
- **Recency filter** — view jobs scraped today, this week, or this month

---

## API endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Main dashboard |
| `GET /api/jobs` | Paginated job listings with search, location, recency filters |
| `GET /api/top-companies` | Top 10 hiring companies |
| `GET /api/top-locations` | Top 8 job locations |
| `GET /api/top-skills` | Top 12 in-demand skills |
| `GET /api/locations-list` | All unique locations for dropdown |

---

## Deployment on Railway

1. Push this repo to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Add a MySQL plugin to your project
4. Set environment variables in Railway dashboard:
   - `SCRAPE_URL` and `PAGES_TO_SCRAPE` (MySQL vars are injected automatically)
5. Railway detects the `Procfile` and deploys automatically

---

## How deduplication works

Every job is stored with a unique key on `(title, company)`. On each scrape run, `INSERT IGNORE` silently skips any job that already exists — so re-running daily never creates duplicate records. New listings are appended and the `scraped_at` timestamp records exactly when each job was first captured.

---

## Author

**Shakti** — Python Developer · Web Scraping · Data Pipelines · Flask  
