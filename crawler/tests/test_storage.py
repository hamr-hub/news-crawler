import pytest
import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def test_storage_import():
    from crawler.services.storage import NewsStorage
    assert NewsStorage is not None


def test_storage_init():
    from crawler.services.storage import NewsStorage
    storage = NewsStorage()
    assert storage is not None


def test_save_news():
    from crawler.services.storage import NewsStorage
    storage = NewsStorage()
    
    news_data = {
        'id': 'test-001',
        'title': 'Test News',
        'content': 'Test content',
        'source': 'test-source',
        'country': 'CN',
        'category': 'general',
        'published_at': datetime.now().isoformat(),
        'crawled_at': datetime.now().isoformat()
    }
    
    result = storage.save_news(news_data)
    assert result is True


def test_save_multiple_news():
    from crawler.services.storage import NewsStorage
    storage = NewsStorage()
    
    news_list = [
        {
            'id': f'test-{i:03d}',
            'title': f'News {i}',
            'content': f'Content {i}',
            'source': 'test-source',
            'country': 'CN',
            'category': 'general',
            'published_at': datetime.now().isoformat(),
            'crawled_at': datetime.now().isoformat()
        }
        for i in range(5)
    ]
    
    result = storage.save_news_batch(news_list)
    assert result is True


def test_load_news():
    from crawler.services.storage import NewsStorage
    storage = NewsStorage()
    
    test_date = datetime.now().strftime('%Y-%m-%d')
    result = storage.load_news(date=test_date)
    assert isinstance(result, list)


def test_json_serialization():
    from crawler.services.storage import NewsStorage
    storage = NewsStorage()
    
    news_data = {
        'id': 'test-002',
        'title': 'Test News with special chars: 你好世界',
        'content': 'Content with "quotes" and \'apostrophes\'',
        'source': 'test-source',
        'country': 'CN',
        'category': 'general',
        'published_at': datetime.now().isoformat(),
        'crawled_at': datetime.now().isoformat()
    }
    
    json_str = storage.to_json(news_data)
    assert isinstance(json_str, str)
    assert 'test-002' in json_str
