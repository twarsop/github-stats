from datetime import datetime
from pydantic.dataclasses import dataclass

file_extension_to_language_map = dict()
file_extension_to_language_map["cs"] = "C#"
file_extension_to_language_map["cshtml"] = "CSHTML"
file_extension_to_language_map["css"] = "CSS"
file_extension_to_language_map["Dockerfile"] = "Dockerfile"
file_extension_to_language_map["html"] = "HTML"
file_extension_to_language_map["ipynb"] = "Jupyter Notebook"
file_extension_to_language_map["js"] = "JS"
file_extension_to_language_map["Makefile"] = "Makefile"
file_extension_to_language_map["md"] = "Markdown"
file_extension_to_language_map["py"] = "Python"
file_extension_to_language_map["sql"] = "SQL"
file_extension_to_language_map["yml"] = "YML"

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

def map_filename_to_language(commit_filenames):
    commit_languages = []

    for commit_filename in commit_filenames:
        split_filename = commit_filename.filename.split(".")

        if split_filename[-1] not in file_extensions_to_ignore:
            filename_to_language_match = None
            for filename, language in file_extension_to_language_map.items():
                if split_filename[-1] == filename:
                    filename_to_language_match = language
            
            if filename_to_language_match is None:
                print(f"Encountered unknown file extension: {split_filename[-1]} in filename: {commit_filename.filename}")

            if filename_to_language_match:
                commit_languages.append(CommitLanguage(commit_filename.datetime, filename_to_language_match, commit_filename.additions))

    return commit_languages