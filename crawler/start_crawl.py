#!/usr/bin/env python3
"""News Crawler Startup - Main entry point for the crawler."""

import argparse
import asyncio
import logging
import sys
from datetime import datetime
from pathlib import Path

import yaml

from crawler.services.search_engine import SearchEngine
from crawler.services.site_classifier import SiteClassifier
from crawler.services.deduplicator import Deduplicator
from crawler.services.storage import NewsStorage
from crawler.workers.news_spider import NewsSpider, ScrapySpider


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NewsCrawler:
    """Main crawler orchestrator."""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.search_engine = SearchEngine(self.config)
        self.classifier = SiteClassifier()
        self.deduplicator = Deduplicator()
        self.storage = NewsStorage()
        
    def _load_config(self, config_path: str) -> dict:
        """Load configuration."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
            
    def discover_sites(self, max_per_engine: int = 20) -> list:
        """Discover news sites from search engines."""
        logger.info("Discovering news sites...")
        
        sites = self.search_engine.discover_news_sites(max_per_engine)
        logger.info(f"Found {len(sites)} sites")
        
        classified_sites = []
        for site in sites:
            classification = self.classifier.classify_site(site['url'])
            classified_sites.append({
                **site,
                **classification
            })
            
        return classified_sites
    
    def crawl_sites(self, sites: list) -> list:
        """Crawl news from sites."""
        logger.info(f"Crawling {len(sites)} sites...")
        
        spider = NewsSpider(self.config)
        articles = []
        
        asyncio.run(spider.initialize())
        
        for site in sites:
            try:
                url = site['url']
                article = asyncio.run(spider.crawl_page(url))
                if article:
                    article['source'] = site.get('title', url)
                    article['country'] = site.get('country', 'OTHER')
                    article['category'] = site.get('category', 'general')
                    articles.append(article)
            except Exception as e:
                logger.error(f"Error crawling {site.get('url')}: {e}")
                
        asyncio.run(spider.close())
        
        logger.info(f"Crawled {len(articles)} articles")
        return articles
    
    def deduplicate_articles(self, articles: list) -> list:
        """Remove duplicate articles."""
        logger.info("Deduplicating articles...")
        return self.deduplicator.deduplicate(articles)
    
    def save_articles(self, articles: list) -> bool:
        """Save articles to storage."""
        if not articles:
            logger.warning("No articles to save")
            return True
            
        logger.info(f"Saving {len(articles)} articles...")
        return self.storage.save_news_batch(articles)
    
    def run(self):
        """Run the complete crawler workflow."""
        logger.info("Starting news crawler...")
        
        sites = self.discover_sites()
        articles = self.crawl_sites(sites)
        unique_articles = self.deduplicate_articles(articles)
        self.save_articles(unique_articles)
        
        logger.info("Crawler finished successfully")
        return unique_articles


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='News Crawler')
    parser.add_argument('--config', default='config.yaml', help='Config file path')
    parser.add_argument('--discover-only', action='store_true', help='Only discover sites')
    parser.add_argument('--max-sites', type=int, default=20, help='Max sites per engine')
    
    args = parser.parse_args()
    
    crawler = NewsCrawler(args.config)
    
    if args.discover_only:
        sites = crawler.discover_sites(args.max_sites)
        print(f"\nDiscovered {len(sites)} sites:")
        for site in sites[:10]:
            print(f"  - {site.get('url')} ({site.get('country')}, {site.get('category')})")
    else:
        crawler.run()


if __name__ == '__main__':
    main()
