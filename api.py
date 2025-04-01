from fastapi import FastAPI, HTTPException
from database import get_recent_events, calculate_average_delta

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "GitHub Events API is running"}

@app.get("/stats/{owner}/{repo}/{event_type}")
async def get_event_stats(owner: str, repo: str, event_type: str):
    repo_name = f"{owner}/{repo}"
    timestamps = get_recent_events(repo_name, event_type)
    
    if not timestamps:
        raise HTTPException(status_code=404, detail="No events found")
    
    avg_time = calculate_average_delta(timestamps)
    
    if avg_time is None:
        raise HTTPException(status_code=404, detail="Not enough events to calculate average time")
    
    return {
        "repo": repo_name,
        "event_type": event_type,
        "average_time_between_events": avg_time
    }
