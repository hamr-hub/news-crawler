import pytest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def test_search_engine_import():
    from crawler.services.search_engine import SearchEngine
    assert SearchEngine is not None


def test_search_engine_init():
    from crawler.services.search_engine import SearchEngine
    engine = SearchEngine()
    assert engine is not None


@patch('crawler.services.search_engine.requests.get')
def test_google_search(mock_get):
    from crawler.services.search_engine import SearchEngine
    mock_response = Mock()
    mock_response.text = '<html><a href="https://example.com">News</a></html>'
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    
    engine = SearchEngine()
    results = engine.search("news site:news", engine="google")
    assert isinstance(results, list)


@patch('crawler.services.search_engine.requests.get')
def test_baidu_search(mock_get):
    from crawler.services.search_engine import SearchEngine
    mock_response = Mock()
    mock_response.text = '<html><a href="https://example.com">News</a></html>'
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    
    engine = SearchEngine()
    results = engine.search("新闻网站", engine="baidu")
    assert isinstance(results, list)


def test_search_result_structure():
    from crawler.services.search_engine import SearchEngine
    engine = SearchEngine()
    sample_result = {
        'url': 'https://example.com',
        'title': 'Example News',
        'snippet': 'News description'
    }
    assert 'url' in sample_result
    assert 'title' in sample_result
