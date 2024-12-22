from datetime import datetime
from pydantic.dataclasses import dataclass

@dataclass
class CommitLanguage:
    datetime: datetime
    language: str
    additions: int

def map_filenames_to_languages(commit_filenames, file_extensions_to_languages, file_extensions_to_ignore):
    commit_languages = []

    for commit_filename in commit_filenames:
        split_filename = commit_filename.filename.split(".")

        if split_filename[-1] not in file_extensions_to_ignore:
            filename_to_language_match = None
            for filename, language in file_extensions_to_languages.items():
                if split_filename[-1] == filename:
                    filename_to_language_match = language
            
            if filename_to_language_match is None:
                print(f"Encountered unknown file extension: {split_filename[-1]} in filename: {commit_filename.filename}")

            if filename_to_language_match:
                commit_languages.append(CommitLanguage(commit_filename.datetime, filename_to_language_match, commit_filename.additions))

    return commit_languages