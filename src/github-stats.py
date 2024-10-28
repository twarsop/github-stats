from dataclasses import dataclass
from datetime import datetime
import os
import requests

HEADERS = {"Authorization": f"token {os.environ['token']}"}
GITHUB_API_BASE_URL = "https://api.github.com"

@dataclass
class CommitFile:
    datetime: datetime
    filename: str
    additions: int

def get_commit_files(github_username, commits_since_date, commits_until_date):
    commit_files = []
    
    repositories_data = None
    
    url = f"{GITHUB_API_BASE_URL}/users/{github_username}/repos"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        repositories_data = response.json()
    else:
        return None
    
    if repositories_data:
        for repo in repositories_data:
            url = f"{GITHUB_API_BASE_URL}/repos/{github_username}/{repo['name']}/commits?since={commits_since_date}&until={commits_until_date}"
            commits = requests.get(url, headers=HEADERS)
            for commit in commits.json():
                commit_url = f"{GITHUB_API_BASE_URL}/repos/{github_username}/{repo['name']}/commits/{commit['sha']}"
                commit_info = requests.get(commit_url, headers=HEADERS)
                for file in commit_info.json()["files"]:
                    commit_files.append(CommitFile(datetime=commit["commit"]["author"]["date"], filename=file["filename"], additions=file["additions"]))
                break

            break
    else:
        print("Failed to retrieve repositories.")

    return commit_files
    

if __name__ == "__main__":    
    commit_files = get_commit_files("twarsop", "2023-10-01", "2023-11-01")

    print(commit_files)