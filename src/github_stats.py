# Todo:
# rename filename_to_language_map to file_extension
# split into files: get github commits (datetime, filename, additions) -> map fileame to language (datetime, language, additions) -> aggregate (year, total additions, [language, additions, percentageß])
# config in file
# unit tests
# instructions in readme

# Done:

from aggregate import aggregate_language_stats_by_year
import argparse
from github_repository import get_commit_files
from map import map_filename_to_language
import json
from pydantic.json import pydantic_encoder

if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--github_username", type=str, required=True)
    parser.add_argument("-s", "--commits_since_date", type=str, required=True)
    parser.add_argument("-t", "--commits_until_date", type=str, required=True)
    args = parser.parse_args()

    commit_files = get_commit_files(args.github_username, args.commits_since_date, args.commits_until_date)

    commit_languages = map_filename_to_language(commit_files)

    yearly_language_stats = aggregate_language_stats_by_year(commit_languages)

    print(json.dumps(yearly_language_stats, indent=4, default=pydantic_encoder))