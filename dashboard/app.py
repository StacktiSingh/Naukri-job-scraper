import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, jsonify, request
import mysql.connector
import pandas as pd
from config import DB_CONFIG


app = Flask(__name__)

def get_df():
    conn = mysql.connector.connect(**DB_CONFIG)
    df = pd.read_sql("SELECT * FROM jobs", conn)
    conn.close()
    return df

@app.route("/")
def index():
    df = get_df()
    total = len(df)
    companies = df["company"].nunique()
    locations = df["location"].nunique()
    with_salary = int(df["salary"].notna().sum())
    return render_template("index.html",
        total=total,
        companies=companies,
        locations=locations,
        with_salary=with_salary
    )

@app.route("/api/top-companies")
def top_companies():
    df = get_df()
    data = df["company"].value_counts().head(10)
    return jsonify({"labels": data.index.tolist(), "values": data.values.tolist()})

@app.route("/api/top-locations")
def top_locations():
    df = get_df()
    data = df["location"].value_counts().head(8)
    return jsonify({"labels": data.index.tolist(), "values": data.values.tolist()})

@app.route("/api/top-skills")
def top_skills():
    df = get_df()
    skills_series = df["skills"].dropna().str.split(r"[\n,]+").explode().str.strip()
    skills_series = skills_series[skills_series.str.len() > 1]
    data = skills_series.value_counts().head(12)
    return jsonify({"labels": data.index.tolist(), "values": data.values.tolist()})

@app.route("/api/jobs")
def jobs():
    df = get_df()
    search = request.args.get("search", "").lower()
    location = request.args.get("location", "")
    page = int(request.args.get("page", 1))
    per_page = 12

    if search:
        df = df[df["title"].str.lower().str.contains(search, na=False) |
                df["company"].str.lower().str.contains(search, na=False) |
                df["skills"].str.lower().str.contains(search, na=False)]
    if location:
        df = df[df["location"].str.contains(location, na=False, case=False)]

    total = len(df)
    df = df.sort_values("scraped_at", ascending=False)
    df = df.iloc[(page - 1) * per_page: page * per_page]
    df = df.fillna("—")

    return jsonify({
        "jobs": df[["title","company","location","experience","salary","skills","posted_date","job_url"]].to_dict(orient="records"),
        "total": total,
        "pages": (total + per_page - 1) // per_page,
        "page": page
    })

@app.route("/api/locations-list")
def locations_list():
    df = get_df()
    locs = df["location"].dropna().unique().tolist()
    return jsonify(sorted(locs))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)