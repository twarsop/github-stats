import argparse
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
    
    repositories_json = get_github_json(f"users/{github_username}/repos")
    
    if repositories_json:
        for repo in repositories_json:
            commits_json = get_github_json(f"repos/{github_username}/{repo['name']}/commits?since={commits_since_date}&until={commits_until_date}")
            if commits_json:
                for commit in commits_json:
                    commit_json = get_github_json(f"repos/{github_username}/{repo['name']}/commits/{commit['sha']}")
                    if commit_json:
                        for file in commit_json["files"]:
                            commit_files.append(CommitFile(datetime=datetime.strptime(commit["commit"]["author"]["date"], '%Y-%m-%dT%H:%M:%SZ'), filename=file["filename"], additions=file["additions"]))
                        break
            break

    return commit_files
    
def get_github_json(endpoint):
    url = f"{GITHUB_API_BASE_URL}/{endpoint}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
@dataclass
class FilenameToLanguage:
    index: int
    filename_part: str
    language: str

filename_to_language_map = []
filename_to_language_map.append(FilenameToLanguage(0, "Dockerfile", "Dockerfile"))
filename_to_language_map.append(FilenameToLanguage(1, "md", "Markdown"))

def calculate_yearly_language_additions(commit_files):
    yearly_language_additions = dict()

    for commit_file in commit_files:
        if commit_file.datetime.year not in yearly_language_additions:
            yearly_language_additions[commit_file.datetime.year] = dict()

        split_filename = commit_file.filename.split(".")
        filename_to_language_match = None
        for filename_to_language in filename_to_language_map:
            if filename_to_language.index < len(split_filename) and split_filename[filename_to_language.index] == filename_to_language.filename_part:
                filename_to_language_match = filename_to_language.language
        
        if filename_to_language_match is None:
            raise(f"No language match for filename: {commit_file.filename}")

        if filename_to_language_match not in yearly_language_additions[commit_file.datetime.year]:
            yearly_language_additions[commit_file.datetime.year][filename_to_language_match] = 0

        yearly_language_additions[commit_file.datetime.year][filename_to_language_match] += commit_file.additions

    return yearly_language_additions

if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--github_username", type=str, required=True)
    parser.add_argument("-s", "--commits_since_date", type=str, required=True)
    parser.add_argument("-t", "--commits_until_date", type=str, required=True)
    args = parser.parse_args()

    commit_files = get_commit_files(args.github_username, args.commits_since_date, args.commits_until_date)

    yearly_language_additions = calculate_yearly_language_additions(commit_files)
    
    print(yearly_language_additions)