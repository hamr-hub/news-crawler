import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def test_classifier_import():
    from crawler.services.site_classifier import SiteClassifier
    assert SiteClassifier is not None


def test_classifier_init():
    from crawler.services.site_classifier import SiteClassifier
    classifier = SiteClassifier()
    assert classifier is not None


def test_classify_country_by_url():
    from crawler.services.site_classifier import SiteClassifier
    classifier = SiteClassifier()
    
    result = classifier.classify_country("https://news.sina.com.cn")
    assert result in ['CN', 'US', 'UK', 'JP', 'RU', 'OTHER']


def test_classify_category():
    from crawler.services.site_classifier import SiteClassifier
    classifier = SiteClassifier()
    
    result = classifier.classify_category("https://news.example.com")
    assert result in ['general', 'technology', 'business', 'sports', 'entertainment', 'politics', 'OTHER']


def test_classify_news_type():
    from crawler.services.site_classifier import SiteClassifier
    classifier = SiteClassifier()
    
    sample_urls = [
        "https://tech.example.com",
        "https://business.example.com",
        "https://sports.example.com"
    ]
    
    for url in sample_urls:
        category = classifier.classify_category(url)
        assert category is not None


def test_load_sites_config():
    from crawler.services.site_classifier import SiteClassifier
    classifier = SiteClassifier()
    config = classifier.load_sites_config()
    assert isinstance(config, dict)
