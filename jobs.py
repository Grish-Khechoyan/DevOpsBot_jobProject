import requests
from config import API_URL

def get_jobs(limit=20):
    try:
        res = requests.get(API_URL, timeout=10)
        res.raise_for_status()
        data = res.json()
        return data.get("jobs", [])[:limit]
    except Exception as e:
        print("Error:", e)
        return []
