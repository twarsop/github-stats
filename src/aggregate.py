from decimal import Decimal
from pydantic.dataclasses import dataclass
from typing import List

@dataclass
class LanguageAddition:
    language: str
    additions: int

@dataclass
class YearlyLanguageAddition:
    year: int
    language_additions: List[LanguageAddition]

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

def aggregate_language_stats_by_year(commit_languages):
    yearly_language_additions_dict = dict()

    for commit_language in commit_languages:
        if commit_language.datetime.year not in yearly_language_additions_dict:
            yearly_language_additions_dict[commit_language.datetime.year] = dict()

        if commit_language.language not in yearly_language_additions_dict[commit_language.datetime.year]:
            yearly_language_additions_dict[commit_language.datetime.year][commit_language.language] = 0

        yearly_language_additions_dict[commit_language.datetime.year][commit_language.language] += commit_language.additions

    yearly_language_additions = []

    for year in yearly_language_additions_dict:
        yearly_language_addition = YearlyLanguageAddition(year=year, language_additions=[])
        for language in yearly_language_additions_dict[year]:
            yearly_language_addition.language_additions.append(LanguageAddition(language=language, additions=yearly_language_additions_dict[year][language]))
        
        yearly_language_additions.append(yearly_language_addition)

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