from github_client import get_repo_events
from dotenv import load_dotenv
import os
from database import init_db, insert_events, get_recent_events, calculate_average_delta
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "GitHub Events API is running"}

def update_github_events():
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")

    repositories = [
        {"owner": "Meituan-Dianping", "repo": "Robust"},
        {"owner": "Meituan-Dianping", "repo": "Leaf"},
        {"owner": "tiana-sky", "repo": "portfolio"},
        {"owner": "tiana-sky", "repo": "capstone"},
    ]

    for repo in repositories:
        owner = repo["owner"]
        repo_name = repo["repo"]
        repo_full = f"{owner}/{repo_name}"
        events = get_repo_events(owner, repo_name, token=token)
        insert_events(events, f"{owner}/{repo_name}")

    print("Data from GitHub are updated.")


if __name__ == "__main__":
    load_dotenv() 
    token = os.getenv("GITHUB_TOKEN")

    owner = "octocat"
    repo = "Hello-World"

    init_db() 

    events = get_repo_events(owner, repo, token=token)

    insert_events(events, f"{owner}/{repo}")
    for event in events[:5]:
        print(f"{event['type']} at {event['created_at']}")

    repo_full = f"{owner}/{repo}"
    event_type = "PushEvent"  

    timestamps = get_recent_events(repo_full, event_type)
    avg_time = calculate_average_delta(timestamps)

    if avg_time is not None:
        print(f"\nAverage time between {event_type}s: {avg_time:.2f} seconds")
    else:
        print(f"\nNot enough {event_type} events to calculate average.")

