from datetime import datetime
from pydantic.dataclasses import dataclass

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
class CommitLanguage:
    datetime: datetime
    language: str
    additions: int

def map_filename_to_language(commit_files):
    commit_languages = []

    for commit_file in commit_files:
        split_filename = commit_file.filename.split(".")

        if split_filename[-1] not in file_extensions_to_ignore:
            filename_to_language_match = None
            for filename, language in filename_to_language_map.items():
                if split_filename[-1] == filename:
                    filename_to_language_match = language
            
            if filename_to_language_match is None:
                print(f"Encountered unknown file extension: {split_filename[-1]} in filename: {commit_file.filename}")

            if filename_to_language_match:
                commit_languages.append(CommitLanguage(commit_file.datetime, filename_to_language_match, commit_file.additions))

    return commit_languages