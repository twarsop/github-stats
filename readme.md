# github-stats

[![Unit Tests](https://github.com/twarsop/github-stats/actions/workflows/python-app.yml/badge.svg)](https://github.com/twarsop/github-stats/actions/workflows/python-app.yml)

A python script for calculating stats about the languages committed in github repos. Specifically, the percentage of additions made to an account's github repos per lanaguage aggregated by year and per language for all time.

## Example Output

```
{
    "all_time_language_stats": [
        {
            "language": "Python",
            "additions": 210052,
            "percentage": 48.82534384290499
        },
        {
            "language": "CSS",
            "additions": 86686,
            "percentage": 20.149647498553037
        },
        {
            "language": "JS",
            "additions": 62630,
            "percentage": 14.557972715713918
        },
        ...
    ],
    "yearly_language_stats": [
        {
            "year": 2023,
            "total_additions": 2302,
            "language_stats": [
                {
                    "language": "C#",
                    "additions": 1574,
                    "percentage": 68.375325803649
                },
                {
                    "language": "CSHTML",
                    "additions": 257,
                    "percentage": 11.164205039096437
                },
                ....
            ]
        },
        {
            "year": 2024,
            "total_additions": 404333,
            "language_stats": [
                {
                    "language": "Python",
                    "additions": 163743,
                    "percentage": 40.49706553756434
                },
                {
                    "language": "CSS",
                    "additions": 129517,
                    "percentage": 32.032260537725094
                },
                ....
            ]
        }
    ]
}
```

## Config

The file `src/config.json` contains some config for the main script. Namely:
1. `file_extensions_to_languages`: a dictionary of file extensions to languages, e.g. `"cs": "C#"`
2. `file_extensions_to_ignore`: file extensions that appear in this array will not be included in the aggregated stats returned by the script

## Running Locally

### `.env`

You need to add a `.env` file in the root directory which needs to contain a `token` environment variable set to a fine-grained access token you have created. So the contents of this file will look like the following:

```
token=github_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Script and `Makefile`

The main entry point for the code is the `src/github_stats.py` script which has following arguments:
1. `github_username` (`-u`) (required)
2. `commits_since_date` (`-s`) (required)
3. `commits_until_date` (`-t`) (required)
4. `file_output` (`-f`) (optional)

There is included in the root of this repo a `Makefile` which contains a `run` receipe that will: set the env variable from `.env` and execute `src/github_stats.py` with the arguments predfined. But if you are using this `Makefile` from this repo you will need to update the arguments provided to the script as it will currently have my arguments set.

### `pipenv`

If don't have `pipenv`:

```
brew install pipenv
```

```
pipenv shell # To activate pipenv
exit # deactivate and quit
pipenv install <libraryName> # install a library
```

### Run the Script

```
pipenv shell
make run
```

(Only need to execute `pipenv shell` if it's not already activated)

### Run the Unit Tests

```
pipenv shell
pytest
```

(Only need to execute `pipenv shell` if it's not already activated)