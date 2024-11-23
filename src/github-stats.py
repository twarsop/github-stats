# Todo:
# rename filename_to_language_map to file_extension
# split into files
# unit tests
# instructions in readme

# Done:

import argparse
from datetime import datetime
import os
import requests
from typing import List
import json
from pydantic.dataclasses import dataclass
from pydantic.json import pydantic_encoder
from decimal import Decimal

HEADERS = {"Authorization": f"token {os.environ['token']}"}
GITHUB_API_BASE_URL = "https://api.github.com"

@dataclass
class CommitFile:
    datetime: datetime
    filename: str
    additions: int

def get_commit_files(github_username, commits_since_date, commits_until_date):
    commit_files = []
    
    repositories_json = get_github_json(f"search/repositories?q=user:twarsop")

    if repositories_json:
        for repo in repositories_json["items"]:
            commits_json = get_github_json(f"repos/{github_username}/{repo['name']}/commits?since={commits_since_date}&until={commits_until_date}")
            if commits_json:
                for commit in commits_json:
                    commit_json = get_github_json(f"repos/{github_username}/{repo['name']}/commits/{commit['sha']}")
                    if commit_json:
                        for file in commit_json["files"]:
                            commit_files.append(CommitFile(datetime=datetime.strptime(commit["commit"]["author"]["date"], '%Y-%m-%dT%H:%M:%SZ'), filename=file["filename"], additions=file["additions"]))

    return commit_files
    
def get_github_json(endpoint):
    url = f"{GITHUB_API_BASE_URL}/{endpoint}"
    response = requests.get(url, headers=HEADERS, params={"username": "twarsop"})
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
filename_to_language_map = dict()
filename_to_language_map["cs"] = "C#"
filename_to_language_map["cshtml"] = "CSHTML"
filename_to_language_map["css"] = "CSS"
filename_to_language_map["Dockerfile"] = "Dockerfile"
filename_to_language_map["html"] = "HTML"
filename_to_language_map["ipynb"] = "Jupyter Notebook"
filename_to_language_map["js"] = "JS"
filename_to_language_map["Makefile"] = "Makefile"
filename_to_language_map["md"] = "Markdown"
filename_to_language_map["py"] = "Python"
filename_to_language_map["sql"] = "SQL"
filename_to_language_map["yml"] = "YML"

file_extensions_to_ignore = [
    "0/apphost",
    "0/calendar-football",
    "1",
    "10",
    "12",
    "asm",
    "bin",
    "build/lambdas/prod/zips/get_fixutres_html/bin/normalizer",
    "build/lambdas/prod/zips/get_fixtures_html/bin/normalizer",
    "build/lambdas/prod/zips/get_fixutres_html_og/bin/normalizer",
    "BuildWithSkipAnalyzers",
    "c",
    "cache",
    "csproj",
    "cmd",
    "cnf",
    "csh",
    "db",
    "db-shm",
    "db-wal",
    "deb",
    "dist-info/AUTHORS",
    "dist-info/INSTALLER",
    "dist-info/LICENSE",
    "dist-info/licenses/AUTHORS",
    "dist-info/licenses/LICENSE",
    "dist-info/METADATA",
    "dist-info/NOTICE",
    "dist-info/RECORD",
    "dist-info/REQUESTED",
    "dist-info/WHEEL",
    "dockerignore",
    "dll",
    "drawio",
    "DS_Store",
    "dylib",
    "editorconfig",
    "enc",
    "exe",
    "fish",
    "gitkeep",
    "gitignore",
    "gz",
    "h",
    "obj",
    "ico",
    "Identifier",
    "j2",
    "jpg",
    "json",
    "lambdas/build/get_raw_fixtures_and_parse_json/bin/normalizer",
    "lambdas/prod/zips/get_fixutres_html/bin/normalizer",
    "lock",
    "log",
    "map",
    "Pipfile",
    "pdb",
    "pdf",
    "pdn",
    "pem",
    "png",
    "props",
    "ps1",
    "PSF",
    "pth",
    "pyc",
    "pyi",
    "rst",
    "sh",
    "sln",
    "so",
    "src/wwwroot/lib/bootstrap/LICENSE",
    "suo",
    "svg",
    "targets",
    "testcase",
    "txt",
    "typed",
    "user",
    "v2",
    "venv/bin/activate",
    "venv/bin/chardetect",
    "venv/bin/dotenv",
    "venv/bin/normalizer",
    "venv/bin/pip",
    "venv/bin/pip3",
    "venv/bin/playwright",
    "venv/bin/python",
    "venv/bin/python3",
    "venv/bin/tqdm",
    "vsidx",
    "webmanifest",
    "wwwroot/lib/bootstrap/LICENSE",
    "xcf",
    "xml",
    "zip"]

@dataclass
class LanguageAddition:
    language: str
    additions: int

@dataclass
class YearlyLanguageAddition:
    year: int
    language_additions: List[LanguageAddition]

def group_yearly_language_additions(commit_files):
    yearly_language_additions_dict = dict()

    for commit_file in commit_files:
        if commit_file.datetime.year not in yearly_language_additions_dict:
            yearly_language_additions_dict[commit_file.datetime.year] = dict()

        split_filename = commit_file.filename.split(".")

        if split_filename[-1] not in file_extensions_to_ignore:
            filename_to_language_match = None
            for filename, language in filename_to_language_map.items():
                if split_filename[-1] == filename:
                    filename_to_language_match = language
            
            if filename_to_language_match is None:
                print(f"Encountered unknown file extension: {split_filename[-1]} in filename: {commit_file.filename}")

            if filename_to_language_match:
                if filename_to_language_match not in yearly_language_additions_dict[commit_file.datetime.year]:
                    yearly_language_additions_dict[commit_file.datetime.year][filename_to_language_match] = 0

                yearly_language_additions_dict[commit_file.datetime.year][filename_to_language_match] += commit_file.additions

    yearly_language_additions = []

    for year in yearly_language_additions_dict:
        yearly_language_addition = YearlyLanguageAddition(year=year, language_additions=[])
        for language in yearly_language_additions_dict[year]:
            yearly_language_addition.language_additions.append(LanguageAddition(language=language, additions=yearly_language_additions_dict[year][language]))
        
        yearly_language_additions.append(yearly_language_addition)

    return yearly_language_additions

@dataclass
class LanguageStats:
    language: str
    additions: int
    percentage: Decimal

@dataclass
class YearlyLanguageStats:
    year: int
    total_additions: int
    language_stats: List[LanguageStats]

def calculate_yearly_language_stats(yearly_language_additions):
    yearly_language_stats = []

    for year in yearly_language_additions:
        total_additions = sum([x.additions for x in year.language_additions])
        yearly_language_stat = YearlyLanguageStats(year=year.year, total_additions=total_additions, language_stats=[])

        for yearly_language_addition in year.language_additions:
            yearly_language_stat.language_stats.append(LanguageStats(language=yearly_language_addition.language, additions=yearly_language_addition.additions, percentage=(yearly_language_addition.additions/total_additions)*100))

        yearly_language_stats.append(yearly_language_stat)

    for yearly_language_stat in yearly_language_stats:
        yearly_language_stat.language_stats.sort(key=lambda x: x.percentage, reverse=True)

    return yearly_language_stats

if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--github_username", type=str, required=True)
    parser.add_argument("-s", "--commits_since_date", type=str, required=True)
    parser.add_argument("-t", "--commits_until_date", type=str, required=True)
    args = parser.parse_args()

    commit_files = get_commit_files(args.github_username, args.commits_since_date, args.commits_until_date)

    yearly_language_additions = group_yearly_language_additions(commit_files)

    yearly_language_stats = calculate_yearly_language_stats(yearly_language_additions)

    print(json.dumps(yearly_language_stats, indent=4, default=pydantic_encoder))