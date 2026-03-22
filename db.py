import sqlite3
from datetime import datetime

DB_NAME = "jobs.db"


def init_db():
    """Initialize the database and create jobs table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            location TEXT,
            url TEXT UNIQUE,
            date_saved TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_new_jobs(jobs):
    """Save jobs to database if they are not already present."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    new_jobs_count = 0

    for job in jobs:
        try:
            cursor.execute('''
                INSERT INTO jobs (title, company, location, url, date_saved)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                job.get('title'),
                job.get('company_name', 'N/A'),
                job.get('candidate_required_location', 'N/A'),
                job.get('url', 'N/A'),
                datetime.now().isoformat()
            ))
            new_jobs_count += 1
        except sqlite3.IntegrityError:
            continue  # Skip duplicates

    conn.commit()
    conn.close()
    return new_jobs_count

def read_jobs_from_db(limit=20):
    """Read latest jobs from database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT title, company, location, url FROM jobs ORDER BY id DESC LIMIT ?', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows