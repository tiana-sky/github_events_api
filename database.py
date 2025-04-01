import sqlite3
from datetime import datetime, timedelta



def init_db():
    conn = sqlite3.connect("events.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY,
            repo_name TEXT,
            event_type TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()

def insert_events(events, repo_name):
    conn = sqlite3.connect("events.db")
    cursor = conn.cursor()

    for event in events:
        try:
            cursor.execute("""
                INSERT INTO events (id, repo_name, event_type, created_at)
                VALUES (?, ?, ?, ?)
            """, (
                event["id"],
                repo_name,
                event["type"],
                event["created_at"]
            ))
        except sqlite3.IntegrityError:
            continue
    conn.commit()
    conn.close()


def get_recent_events(repo_name, event_type):
    conn = sqlite3.connect("events.db")
    cursor = conn.cursor()

    seven_days_ago = (datetime.utcnow() - timedelta(days=7)).isoformat()

    cursor.execute("""
        SELECT created_at FROM events
        WHERE repo_name = ?
          AND event_type = ?
          AND created_at >= ?
        ORDER BY created_at ASC
        LIMIT 500
    """, (repo_name, event_type, seven_days_ago))
    rows = cursor.fetchall()
    conn.close()

    timestamps = [datetime.fromisoformat(ts[0].replace('Z', '+00:00')) for ts in rows]
    return timestamps

def calculate_average_delta(timestamps):
    if len(timestamps) < 2:
        return None

    deltas = [
        (timestamps[i+1] - timestamps[i]).total_seconds()
        for i in range(len(timestamps) - 1)
    ]

    return sum(deltas) / len(deltas)