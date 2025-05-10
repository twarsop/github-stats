from aggregate import *
from map import CommitLanguage
import math

def test_aggregate_stats_multiple_commits_multiple_languages():
    commit_languages = [
        CommitLanguage(datetime="2021-01-01T00:00:00Z", language="Python", additions=200),
        CommitLanguage(datetime="2021-01-01T00:00:00Z", language="JavaScript", additions=150),
        CommitLanguage(datetime="2021-02-01T00:00:00Z", language="Python", additions=100),
        CommitLanguage(datetime="2021-02-01T00:00:00Z", language="JavaScript", additions=50),
        CommitLanguage(datetime="2022-01-01T00:00:00Z", language="Python", additions=200),
        CommitLanguage(datetime="2022-01-01T00:00:00Z", language="JavaScript", additions=100),
    ]

    # Expected all-time stats
    expected_all_time_language_stats = [
        LanguageStats(language="Python", additions=500, percentage=62.5),
        LanguageStats(language="JavaScript", additions=300, percentage=37.5),    
    ]


    # Expected yearly stats
    expected_yearly_language_stats = [
        YearlyLanguageStats(
            year=2021,
            total_additions=500,
            language_stats=[
                LanguageStats(language="Python", additions=300, percentage=60.0),
                LanguageStats(language="JavaScript", additions=200, percentage=40.0),
            ]
        ),
        YearlyLanguageStats(
            year=2022,
            total_additions=300,
            language_stats=[
                LanguageStats(language="Python", additions=200, percentage=66.66),
                LanguageStats(language="JavaScript", additions=100, percentage=33.33),
            ]
        )
    ]

    result = aggregate_stats(commit_languages)

    # All-time stats
    assert len(expected_all_time_language_stats) == len(result.all_time_language_stats)
    
    for i in range(len(expected_all_time_language_stats)):
        assert expected_all_time_language_stats[i].language == result.all_time_language_stats[i].language
        assert expected_all_time_language_stats[i].additions == result.all_time_language_stats[i].additions
        assert math.isclose(expected_all_time_language_stats[i].percentage, result.all_time_language_stats[i].percentage, rel_tol=1e-3)

    # Yearly stats
    assert len(expected_yearly_language_stats) == len(result.yearly_language_stats)

    for i in range(len(expected_yearly_language_stats)):
        assert expected_yearly_language_stats[i].year == result.yearly_language_stats[i].year
        assert expected_yearly_language_stats[i].total_additions == result.yearly_language_stats[i].total_additions
        assert len(expected_yearly_language_stats[i].language_stats) == len(result.yearly_language_stats[i].language_stats)

        for j in range(len(expected_yearly_language_stats[i].language_stats)):
            assert expected_yearly_language_stats[i].language_stats[j].language == result.yearly_language_stats[i].language_stats[j].language
            assert expected_yearly_language_stats[i].language_stats[j].additions == result.yearly_language_stats[i].language_stats[j].additions
            assert math.isclose(expected_yearly_language_stats[i].language_stats[j].percentage, result.yearly_language_stats[i].language_stats[j].percentage, rel_tol=1e-3)
