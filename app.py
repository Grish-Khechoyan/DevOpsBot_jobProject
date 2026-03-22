from flask import Flask, jsonify, request

from config import PORT
from db import init_db, read_jobs_from_db, save_new_jobs
from jobs import get_jobs

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.get("/jobs")
def list_jobs():
    limit = request.args.get("limit", default=20, type=int)
    limit = max(1, min(limit, 100))

    rows = read_jobs_from_db(limit)
    jobs = [
        {
            "title": row[0],
            "company": row[1],
            "location": row[2],
            "url": row[3],
        }
        for row in rows
    ]
    return jsonify({"count": len(jobs), "jobs": jobs}), 200


@app.post("/jobs/refresh")
def refresh_jobs():
    jobs_list = get_jobs()
    if not jobs_list:
        return jsonify({"message": "No jobs fetched from source.", "new_jobs": 0}), 200

    new_jobs = save_new_jobs(jobs_list)
    return jsonify({"message": "Jobs refreshed.", "new_jobs": new_jobs}), 200


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=PORT)
