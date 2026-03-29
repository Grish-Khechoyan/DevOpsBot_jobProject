import os
from datetime import datetime

import psycopg2


def get_db_connection():
    """Create and return a PostgreSQL connection using environment variables."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME", "jobs"),
        user=os.getenv("DB_USER", "jobs_user"),
        password=os.getenv("DB_PASSWORD", "jobs_password"),
    )


def init_db():
    """Initialize PostgreSQL schema for jobs."""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS jobs (
                    id SERIAL PRIMARY KEY,
                    title TEXT,
                    company TEXT,
                    location TEXT,
                    url TEXT UNIQUE,
                    date_saved TIMESTAMP
                )
                """
            )


def save_new_jobs(jobs):
    """Save jobs to database if they are not already present."""
    new_jobs_count = 0

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            for job in jobs:
                cursor.execute(
                    """
                    INSERT INTO jobs (title, company, location, url, date_saved)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (url) DO NOTHING
                    """,
                    (
                        job.get("title"),
                        job.get("company_name", "N/A"),
                        job.get("candidate_required_location", "N/A"),
                        job.get("url", "N/A"),
                        datetime.utcnow(),
                    ),
                )
                if cursor.rowcount == 1:
                    new_jobs_count += 1

    return new_jobs_count


def read_jobs_from_db(limit=20):
    """Read latest jobs from database."""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT title, company, location, url
                FROM jobs
                ORDER BY id DESC
                LIMIT %s
                """,
                (limit,),
            )
            return cursor.fetchall()
