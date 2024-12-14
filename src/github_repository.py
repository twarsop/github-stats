from datetime import datetime
import os
from pydantic.dataclasses import dataclass
import requests

HEADERS = {"Authorization": f"token {os.environ['token']}"}
GITHUB_API_BASE_URL = "https://api.github.com"

@dataclass
class CommitFilename:
    datetime: datetime
    filename: str
    additions: int

def get_commit_filenames(github_username, commits_since_date, commits_until_date):
    commit_filenames = []
    
    repositories_json = get_github_json(f"search/repositories?q=user:{github_username}", github_username)

    if repositories_json:
        for repo in repositories_json["items"]:
            commits_json = get_github_json(f"repos/{github_username}/{repo['name']}/commits?since={commits_since_date}&until={commits_until_date}", github_username)
            if commits_json:
                for commit in commits_json:
                    commit_json = get_github_json(f"repos/{github_username}/{repo['name']}/commits/{commit['sha']}", github_username)
                    if commit_json:
                        for file in commit_json["files"]:
                            commit_filenames.append(CommitFilename(datetime=datetime.strptime(commit["commit"]["author"]["date"], '%Y-%m-%dT%H:%M:%SZ'), filename=file["filename"], additions=file["additions"]))

    return commit_filenames
    
def get_github_json(endpoint, github_username):
    url = f"{GITHUB_API_BASE_URL}/{endpoint}"
    response = requests.get(url, headers=HEADERS, params={"username": github_username})
    if response.status_code == 200:
        return response.json()
    else:
        return None