import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def test_deduplicator_import():
    from crawler.services.deduplicator import Deduplicator
    assert Deduplicator is not None


def test_deduplicator_init():
    from crawler.services.deduplicator import Deduplicator
    dedup = Deduplicator()
    assert dedup is not None


def test_deduplicate_exact_match():
    from crawler.services.deduplicator import Deduplicator
    dedup = Deduplicator()
    
    news_list = [
        {'id': '1', 'title': 'Same Title', 'content': 'Same Content', 'source': 'site1'},
        {'id': '2', 'title': 'Same Title', 'content': 'Same Content', 'source': 'site2'},
    ]
    
    result = dedup.deduplicate(news_list)
    assert len(result) <= 2


def test_deduplicate_similar_title():
    from crawler.services.deduplicator import Deduplicator
    dedup = Deduplicator()
    
    news_list = [
        {'id': '1', 'title': 'Breaking News: Important Event', 'content': 'Content A', 'source': 'site1'},
        {'id': '2', 'title': 'Breaking News: Important Event Updated', 'content': 'Content B', 'source': 'site2'},
    ]
    
    result = dedup.deduplicate(news_list)
    assert isinstance(result, list)


def test_deduplicate_different_news():
    from crawler.services.deduplicator import Deduplicator
    dedup = Deduplicator()
    
    news_list = [
        {'id': '1', 'title': 'News About Tech', 'content': 'Tech content', 'source': 'site1'},
        {'id': '2', 'title': 'News About Sports', 'content': 'Sports content', 'source': 'site2'},
    ]
    
    result = dedup.deduplicate(news_list)
    assert len(result) == 2


def test_similarity_calculation():
    from crawler.services.deduplicator import Deduplicator
    dedup = Deduplicator()
    
    text1 = "This is a test news article"
    text2 = "This is a test news article"
    text3 = "Completely different content"
    
    sim_same = dedup.calculate_similarity(text1, text2)
    sim_diff = dedup.calculate_similarity(text1, text3)
    
    assert sim_same > sim_diff
