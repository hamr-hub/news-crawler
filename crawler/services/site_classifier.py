"""Site Classifier Module - Classifies news sites by country and category."""

import re
from typing import Dict, Optional
import yaml
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class SiteClassifier:
    """Classifies news websites by country and category."""
    
    COUNTRY_PATTERNS = {
        'CN': ['.cn', 'sina', 'sohu', '163', 'ifeng', 'people', 'xinhuanet', 'qq.com', 'toutiao'],
        'US': ['.com', 'cnn', 'bbc', 'reuters', 'apnews', 'nytimes', 'washingtonpost', 'wsj'],
        'UK': ['.co.uk', 'bbc.co.uk', 'theguardian', 'telegraph', 'dailymail'],
        'JP': ['.jp', 'yahoo.co.jp', 'nikkei', 'asahi', 'mainichi'],
        'RU': ['.ru', 'ria', 'tass', 'kommersant', 'lenta'],
    }
    
    CATEGORY_KEYWORDS = {
        'general': ['news', 'headlines', 'latest', 'breaking'],
        'technology': ['tech', 'technology', 'techcrunch', 'verge', 'wired'],
        'business': ['business', 'finance', 'market', 'economy', 'forbes'],
        'sports': ['sports', 'espn', 'sport', 'football', 'basketball'],
        'entertainment': ['entertainment', 'hollywood', 'Variety', 'ew', 'celebrity'],
        'politics': ['politics', 'political', 'government', 'congress'],
    }
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self.sites_config = self._load_config()
        
    def _load_config(self) -> Dict:
        """Load sites configuration."""
        if self.config_path and Path(self.config_path).exists():
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f) or {}
        
        config_file = Path(__file__).parent.parent / "config" / "sites.yaml"
        if config_file.exists():
            with open(config_file, 'r') as f:
                return yaml.safe_load(f) or {}
                
        return {}
        
    def load_sites_config(self) -> Dict:
        """Load sites config (public method)."""
        return self._load_config()
        
    def classify_country(self, url: str) -> str:
        """Classify the country of a news site based on URL.
        
        Args:
            url: The URL of the news site
            
        Returns:
            Country code (CN, US, UK, JP, RU, or OTHER)
        """
        url_lower = url.lower()
        
        for country, patterns in self.COUNTRY_PATTERNS.items():
            for pattern in patterns:
                if pattern in url_lower:
                    return country
                    
        return 'OTHER'
    
    def classify_category(self, url: str) -> str:
        """Classify the category of a news site.
        
        Args:
            url: The URL of the news site
            
        Returns:
            Category name (general, technology, business, etc.)
        """
        url_lower = url.lower()
        
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in url_lower:
                    return category
                    
        return 'general'
    
    def classify_site(self, url: str) -> Dict:
        """Classify a news site by country and category.
        
        Args:
            url: The URL of the news site
            
        Returns:
            Dictionary with country and category
        """
        return {
            'url': url,
            'country': self.classify_country(url),
            'category': self.classify_category(url)
        }
    
    def classify_batch(self, urls: list) -> list:
        """Classify multiple sites.
        
        Args:
            urls: List of URLs
            
        Returns:
            List of classification results
        """
        return [self.classify_site(url) for url in urls]
    
    def get_country_name(self, country_code: str) -> str:
        """Get full country name from code."""
        names = {
            'CN': 'China',
            'US': 'United States',
            'UK': 'United Kingdom',
            'JP': 'Japan',
            'RU': 'Russia',
            'OTHER': 'Other',
        }
        return names.get(country_code, 'Unknown')
    
    def get_category_name(self, category: str) -> str:
        """Get full category name."""
        names = {
            'general': 'General News',
            'technology': 'Technology',
            'business': 'Business',
            'sports': 'Sports',
            'entertainment': 'Entertainment',
            'politics': 'Politics',
        }
        return names.get(category, category.title())
