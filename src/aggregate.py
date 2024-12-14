from decimal import Decimal
from pydantic.dataclasses import dataclass
from typing import List, Dict
from collections import defaultdict

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
    yearly_language_additions = defaultdict(lambda: defaultdict(int))

    # Aggregate additions by year and language
    for commit in commit_languages:
        yearly_language_additions[commit.datetime.year][commit.language] += commit.additions

    yearly_language_stats = []
    for year, languages in yearly_language_additions.items():
        total_additions = sum(languages.values())
        
        language_stats = [
            LanguageStats(
                language=lang,
                additions=additions,
                percentage=Decimal((additions / total_additions) * 100)
            )
            for lang, additions in languages.items()
        ]
        # Sort stats by percentage in descending order
        language_stats.sort(key=lambda x: x.percentage, reverse=True)

        yearly_language_stats.append(YearlyLanguageStats(year, total_additions, language_stats))

    return yearly_language_stats
