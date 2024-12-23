from github_repository import CommitFilename
from map import CommitLanguage, map_filenames_to_languages

def test_commit_filenames_empty_returns_empty():
    commit_languages = map_filenames_to_languages([], {}, [])
    
    assert commit_languages == []

def test_file_extensions_to_languages_empty_returns_empty():
    commit_filenames = [CommitFilename(datetime="2021-01-01T00:00:00Z", filename="test.py", additions=1)]
    
    commit_languages = map_filenames_to_languages(commit_filenames, {}, [])
    
    assert commit_languages == []

def test_commit_filename_extension_exists_in_file_extensions_to_languages_returns_commit_language():
    commit_filenames = [CommitFilename(datetime="2021-01-01T00:00:00Z", filename="test.py", additions=1)]
    
    commit_languages = map_filenames_to_languages(commit_filenames, {"py": "Python"}, [])
    
    assert commit_languages == [CommitLanguage(datetime="2021-01-01T00:00:00Z", language="Python", additions=1)]

def test_commit_filename_extension_does_not_exist_in_file_extensions_to_languages_returns_empty():
    commit_filenames = [CommitFilename(datetime="2021-01-01T00:00:00Z", filename="test.py", additions=1)]
    
    commit_languages = map_filenames_to_languages(commit_filenames, {"java": "Java"}, [])
    
    assert commit_languages == []

def test_commit_filename_extension_exists_in_file_extensions_to_ignore_returns_empty():
    commit_filenames = [CommitFilename(datetime="2021-01-01T00:00:00Z", filename="test.py", additions=1)]
    
    commit_languages = map_filenames_to_languages(commit_filenames, {"py": "Python"}, ["py"])
    
    assert commit_languages == []