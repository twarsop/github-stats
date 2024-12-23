# Todo:
# run unit tests in github
# instructions in readme

from aggregate import aggregate_language_stats_by_year
import argparse
from github_repository import get_commit_filenames
from map import map_filenames_to_languages
import json
from pydantic.json import pydantic_encoder

if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--github_username", type=str, required=True)
    parser.add_argument("-s", "--commits_since_date", type=str, required=True)
    parser.add_argument("-t", "--commits_until_date", type=str, required=True)
    args = parser.parse_args()

    config = None
    with open("config.json", "r") as file:
        config = json.load(file)

    if config:
        commit_filenames = get_commit_filenames(args.github_username, args.commits_since_date, args.commits_until_date)

        commit_languages = map_filenames_to_languages(commit_filenames, config["file_extensions_to_languages"], config["file_extensions_to_ignore"])

        yearly_language_stats = aggregate_language_stats_by_year(commit_languages)

        print(json.dumps(yearly_language_stats, indent=4, default=pydantic_encoder))
    else:
        print("Failed to load config")