from aggregate import *
from map import CommitLanguage
import math

def test_aggregate_language_stats_by_year_empty_returns_empty():
    yearly_language_stats = aggregate_language_stats_by_year([])
    
    assert yearly_language_stats == []

def test_aggregate_language_stats_by_year_single_commit_single_language_returns_yearly_language_stats():
    commit_languages = [
        CommitLanguage(datetime="2021-01-01T00:00:00Z", language="Python", additions=1)
    ]
    
    yearly_language_stats = aggregate_language_stats_by_year(commit_languages)
    
    assert yearly_language_stats == [
        YearlyLanguageStats(
            year=2021,
            total_additions=1,
            language_stats=[
                LanguageStats(language="Python", additions=1, percentage=100)
            ]
        )
    ]

def test_aggregate_language_stats_by_year_single_commit_multiple_languages_returns_yearly_language_stats():
    commit_languages = [
        CommitLanguage(datetime="2021-01-01T00:00:00Z", language="Python", additions=1),
        CommitLanguage(datetime="2021-01-01T00:00:00Z", language="Python", additions=1)
    ]
    
    yearly_language_stats = aggregate_language_stats_by_year(commit_languages)
    
    assert yearly_language_stats == [
        YearlyLanguageStats(
            year=2021,
            total_additions=2,
            language_stats=[
                LanguageStats(language="Python", additions=2, percentage=100)
            ]
        )
    ]

def test_aggregate_language_stats_by_year_multiple_commits_multiple_languages_returns_yearly_language_stats():
    commit_languages = [
        CommitLanguage(datetime="2021-01-01T00:00:00Z", language="Python", additions=1),
        CommitLanguage(datetime="2021-01-01T00:00:00Z", language="Python", additions=1),
        CommitLanguage(datetime="2021-01-01T00:00:00Z", language="C#", additions=1)
    ]
    
    yearly_language_stats = aggregate_language_stats_by_year(commit_languages)
    
    expected = [
        YearlyLanguageStats(
            year=2021,
            total_additions=3,
            language_stats=[
                LanguageStats(language="Python", additions=2, percentage=66.666),
                LanguageStats(language="C#", additions=1, percentage=33.333)
            ]
        )
    ]

    compare_yearly_language_stats(yearly_language_stats, expected)

def test_aggregate_language_stats_by_year_multiple_commits_multiple_years_multiple_languages_returns_yearly_language_stats():
    commit_languages = [
        CommitLanguage(datetime="2021-01-01T00:00:00Z", language="Python", additions=1),
        CommitLanguage(datetime="2021-01-01T00:00:00Z", language="Python", additions=1),
        CommitLanguage(datetime="2021-01-01T00:00:00Z", language="C#", additions=1),
        CommitLanguage(datetime="2022-01-01T00:00:00Z", language="Python", additions=1),
        CommitLanguage(datetime="2022-01-01T00:00:00Z", language="Python", additions=1),
        CommitLanguage(datetime="2022-01-01T00:00:00Z", language="C#", additions=1)
    ]
    
    yearly_language_stats = aggregate_language_stats_by_year(commit_languages)
    
    expected = [
        YearlyLanguageStats(
            year=2021,
            total_additions=3,
            language_stats=[
                LanguageStats(language="Python", additions=2, percentage=66.666),
                LanguageStats(language="C#", additions=1, percentage=33.333)
            ]
        ),
        YearlyLanguageStats(
            year=2022,
            total_additions=3,
            language_stats=[
                LanguageStats(language="Python", additions=2, percentage=66.666),
                LanguageStats(language="C#", additions=1, percentage=33.333)
            ]
        )
    ]

    compare_yearly_language_stats(yearly_language_stats, expected)

def compare_yearly_language_stats(actual, expected):
    assert len(actual) == len(expected)

    for i in range(len(expected)):
        assert actual[i].year == expected[i].year
        assert actual[i].total_additions == expected[i].total_additions
        assert len(actual[i].language_stats) == len(expected[i].language_stats)
        
        for j in range(len(expected[i].language_stats)):
            assert actual[i].language_stats[j].language == expected[i].language_stats[j].language
            assert actual[i].language_stats[j].additions == expected[i].language_stats[j].additions
            assert math.isclose(actual[i].language_stats[j].percentage, expected[i].language_stats[j].percentage, rel_tol=1e-3)