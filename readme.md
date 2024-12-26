# github-stats

[![Unit Tests](https://github.com/twarsop/github-stats/actions/workflows/python-app.yml/badge.svg)](https://github.com/twarsop/github-stats/actions/workflows/python-app.yml)

A python script for calculating the percentage of additions you make to your github repos per langauge aggregated by year.

## Example Output

```
[
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
            {
                "language": "Python",
                "additions": 161,
                "percentage": 6.993918331885316
            },
            {
                "language": "HTML",
                "additions": 155,
                "percentage": 6.733275412684622
            },
            {
                "language": "Markdown",
                "additions": 119,
                "percentage": 5.169417897480452
            },
            {
                "language": "Dockerfile",
                "additions": 21,
                "percentage": 0.9122502172024326
            },
            {
                "language": "CSS",
                "additions": 15,
                "percentage": 0.6516072980017376
            }
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
            {
                "language": "JS",
                "additions": 93945,
                "percentage": 23.234561611345104
            },
            {
                "language": "HTML",
                "additions": 15504,
                "percentage": 3.834463177628341
            },
            {
                "language": "C#",
                "additions": 628,
                "percentage": 0.1553175229328301
            },
            {
                "language": "CSHTML",
                "additions": 600,
                "percentage": 0.14839253783391412
            },
            {
                "language": "Markdown",
                "additions": 244,
                "percentage": 0.06034629871912508
            },
            {
                "language": "SQL",
                "additions": 62,
                "percentage": 0.015333895576171127
            },
            {
                "language": "YML",
                "additions": 40,
                "percentage": 0.009892835855594275
            },
            {
                "language": "Makefile",
                "additions": 28,
                "percentage": 0.006924985098915993
            },
            {
                "language": "Dockerfile",
                "additions": 22,
                "percentage": 0.005441059720576851
            }
        ]
    }
]
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

The main entry point for the code is the `src/github_stats.py` script which has three mandatory arguments:
1. `github_username`
2. `commits_since_date`
3. `commits_until_date`

There is include in the root of this repo a `Makefile` which contains a `run` receipe that will: set the env variable from `.env` and execute `src/github_stats.py` with the arguments predfined. But if you are using this `Makefile` from this repo you will need to update the arguments provided to the script as it will currently have my arguments.

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