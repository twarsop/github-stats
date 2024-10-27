from dataclasses import dataclass
from datetime import datetime
import os
import requests

@dataclass
class CommitFile:
    datetime: datetime
    filename: str
    additions: int

token = os.environ["token"]
headers = {'Authorization': 'token ' + token}
base_url = "https://api.github.com"

def get_user_repos(username):
    url = f"{base_url}/users/{username}/repos"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repositories_data = response.json()
        return repositories_data
    else:
        return None

if __name__ == "__main__":    
    username = "twarsop" # github username
    user_repos = get_user_repos(username)

    commit_files = []

    if user_repos:
        for repo in user_repos:
            url = f"{base_url}/repos/{username}/{repo['name']}/commits?since=2023-10-01&until=2023-11-01"
            commits = requests.get(url, headers=headers)
            for commit in commits.json():
                commit_url = f"{base_url}/repos/{username}/{repo['name']}/commits/{commit['sha']}"
                commit_info = requests.get(commit_url, headers=headers)
                for file in commit_info.json()["files"]:
                    commit_files.append(CommitFile(datetime=commit["commit"]["author"]["date"], filename=file["filename"], additions=file["additions"]))
                break
            break
    else:
        print(f"Failed to retrieve repositories.")

    print(commit_files)