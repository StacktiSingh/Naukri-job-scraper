# data/cleaner.py

import pandas as pd

def clean_jobs(jobs: list[dict]) -> list[dict]:
    df = pd.DataFrame(jobs)

    # Drop rows with no title or company (useless records)
    df.dropna(subset=["title", "company"], inplace=True)

    # Strip whitespace from all string columns
    str_cols = ["title", "company", "location", "experience", "salary", "skills", "posted_date"]
    for col in str_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Replace literal "None" strings left from failed scrapes
    df.replace("None", None, inplace=True)

    # Remove exact duplicates
    df.drop_duplicates(subset=["title", "company"], inplace=True)

    print(f"Clean records: {len(df)}")
    return df.to_dict(orient="records")