import requests

GITHUB_API_URL = "https://api.github.com"

def get_repo_events(owner: str, repo: str, token: str = None):
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/events"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching events: {response.status_code} - {response.text}")
        return []