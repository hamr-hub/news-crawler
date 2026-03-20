#!/usr/bin/env python3
import argparse
import logging
import yaml
import subprocess
from pathlib import Path

from crawler.services.search_engine import SearchEngine
from crawler.services.site_classifier import SiteClassifier
from crawler.services.deduplicator import Deduplicator
from crawler.services.storage import NewsStorage

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NewsCrawler:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.search_engine = SearchEngine(self.config)
        self.classifier = SiteClassifier()
        self.deduplicator = Deduplicator()
        self.storage = NewsStorage()
        
    def _load_config(self, config_path: str) -> dict:
        path = Path(config_path)
        if not path.exists() and path.name == "config.yaml":
            parent_path = Path("..") / "config.yaml"
            if parent_path.exists():
                path = parent_path
                
        if not path.exists():
            logger.warning(f"Config file {config_path} not found.")
            return {}
            
        with open(path, 'r') as f:
            return yaml.safe_load(f)
            
    def discover_sites(self, max_per_engine: int = 20) -> list:
        logger.info("Discovering news sites...")
        sites = self.search_engine.discover_news_sites(max_per_engine)
        logger.info(f"Found {len(sites)} sites")
        classified_sites = []
        for site in sites:
            classification = self.classifier.classify_site(site['url'])
            classified_sites.append({**site, **classification})
        return classified_sites
    
    def run_scrapy(self):
        logger.info("Running discovery spider...")
        subprocess.run(["scrapy", "crawl", "discovery_spider"])
        logger.info("Running news spider...")
        subprocess.run(["scrapy", "crawl", "news_spider"])

    def run(self):
        logger.info("Starting news crawler...")
        self.run_scrapy()
        logger.info("Crawler finished successfully")

def main():
    parser = argparse.ArgumentParser(description="News Crawler")
    parser.add_argument("--config", default="config.yaml", help="Config file path")
    parser.add_argument("--discover-only", action="store_true", help="Only discover sites")
    parser.add_argument("--max-sites", type=int, default=20, help="Max sites per engine")
    args = parser.parse_args()
    
    crawler = NewsCrawler(args.config)
    if args.discover_only:
        sites = crawler.discover_sites(args.max_sites)
        print("Discovered {} sites:".format(len(sites)))
        for site in sites[:10]:
            print("  - {} ({}, {})".format(site.get("url"), site.get("country"), site.get("category")))
    else:
        crawler.run()

if __name__ == '__main__':
    main()
