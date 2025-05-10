from aggregate import *
from map import CommitLanguage
import math

def test_aggregate_all_time_language_stats_returns_correctly_aggegrated_stats():
    commit_languages = [
        CommitLanguage(datetime="2021-01-01T00:00:00Z", language="C#", additions=1),
        CommitLanguage(datetime="2021-01-01T00:00:00Z", language="Python", additions=1),
        CommitLanguage(datetime="2021-01-01T00:00:00Z", language="Python", additions=1)
    ]
    
    all_time_language_stats = aggregate_all_time_language_stats(commit_languages)
    
    expected = [
        LanguageStats(language="Python", additions=2, percentage=66.666),
        LanguageStats(language="C#", additions=1, percentage=33.333)
    ]
    
    assert len(all_time_language_stats) == len(expected)
    
    for i in range(len(all_time_language_stats)):
        assert all_time_language_stats[i].language == expected[i].language
        assert all_time_language_stats[i].additions == expected[i].additions
        assert math.isclose(all_time_language_stats[i].percentage, expected[i].percentage, rel_tol=1e-3)