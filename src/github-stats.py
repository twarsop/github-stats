from dataclasses import dataclass
from datetime import datetime
import os
import requests

HEADERS = {"Authorization": "token " + os.environ["token"]}
GITHUB_API_BASE_URL = "https://api.github.com"

@dataclass
class CommitFile:
    datetime: datetime
    filename: str
    additions: int

def get_user_repos(username):
    url = f"{GITHUB_API_BASE_URL}/users/{username}/repos"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        repositories_data = response.json()
        return repositories_data
    else:
        return None

def get_user_repo_commit_files(username, repo):
    commit_files = []
    
    url = f"{GITHUB_API_BASE_URL}/repos/{username}/{repo['name']}/commits?since=2023-10-01&until=2023-11-01"
    commits = requests.get(url, headers=HEADERS)
    for commit in commits.json():
        commit_url = f"{GITHUB_API_BASE_URL}/repos/{username}/{repo['name']}/commits/{commit['sha']}"
        commit_info = requests.get(commit_url, headers=HEADERS)
        for file in commit_info.json()["files"]:
            commit_files.append(CommitFile(datetime=commit["commit"]["author"]["date"], filename=file["filename"], additions=file["additions"]))
        break

    return commit_files

if __name__ == "__main__":    
    username = "twarsop"
    user_repos = get_user_repos(username)

    commit_files = []

    if user_repos:
        for repo in user_repos:
            commit_files += get_user_repo_commit_files(username, repo)
            break
    else:
        print(f"Failed to retrieve repositories.")

    print(commit_files)