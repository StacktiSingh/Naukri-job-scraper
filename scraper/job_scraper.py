# scraper/naukri_scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import random
from config import SCRAPE_URL, PAGES_TO_SCRAPE

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

def scrape_page(url):
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        # Wait for the dynamic content to load
        time.sleep(5) 
        soup = BeautifulSoup(driver.page_source, "html.parser")
        job_cards = soup.find_all("div", class_="srp-jobtuple-wrapper")
        print(f"Found {len(job_cards)} job cards.")
        jobs = []
        for card in job_cards:
            title_tag    = card.find("a", class_="title")
            skills_tag = card.find_all("li", class_="dot-gt")
            date_tag     = card.find("span", class_="job-post-day")
            company_tag  = card.find("a", class_="comp-name")
            details = card.find("div", class_="row3")
            location_tag = details.find('span', class_='loc-wrap')
            salary_tag = details.find('span', class_='sal-wrap')
            exp_tag = details.find('span', class_='exp-wrap')

            jobs.append({
                "title":       title_tag.text.strip()    if title_tag    else None,
                "company":     company_tag.text.strip()  if company_tag  else None,
                "location":    location_tag.text.strip() if location_tag else None,
                "experience":  exp_tag.text.strip()      if exp_tag      else None,
                "salary":      salary_tag.text.strip()   if salary_tag   else None,
                "skills": ", ".join([skill.text.strip() for skill in skills_tag]) if skills_tag else None,
                "posted_date": date_tag.text.strip()     if date_tag     else None,
                "job_url":     title_tag["href"]         if title_tag    else None,
            })
        return jobs
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []

def run_scraper():
    all_jobs = []
    for page in range(1, PAGES_TO_SCRAPE + 1):
        url = f"{SCRAPE_URL}-{page}" if page > 1 else SCRAPE_URL
        print(f"Scraping page {page}: {url}")
        jobs = scrape_page(url)
        print(f"  Found {len(jobs)} jobs")
        all_jobs.extend(jobs)
        time.sleep(random.uniform(2, 4))  # polite delay between pages
    print(f"Total scraped: {len(all_jobs)} jobs")
    return all_jobs

if __name__ == "__main__":
    jobs = run_scraper()
    for j in jobs[:3]:  # preview first 3
        print(j)