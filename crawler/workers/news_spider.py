"""News Spider Worker - Crawls news from websites using Playwright."""

import asyncio
import logging
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class NewsSpider:
    """Crawls news from websites using Playwright."""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.browser = None
        self.context = None
        
    async def initialize(self):
        """Initialize Playwright browser."""
        try:
            from playwright.async_api import async_playwright
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=True)
            self.context = await self.browser.new_context(
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            )
            logger.info("Playwright browser initialized")
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            
    async def close(self):
        """Close browser."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
            
    async def crawl_page(self, url: str) -> Optional[Dict]:
        """Crawl a single news page.
        
        Args:
            url: URL to crawl
            
        Returns:
            Dictionary with crawled data
        """
        if not self.context:
            await self.initialize()
            
        try:
            page = await self.context.new_page()
            await page.goto(url, timeout=30000, wait_until='networkidle')
            
            title = await page.title()
            
            article = {
                'url': url,
                'title': title,
                'crawled_at': datetime.now().isoformat()
            }
            
            await page.close()
            return article
            
        except Exception as e:
            logger.error(f"Error crawling {url}: {e}")
            return None
    
    async def crawl_list(self, urls: List[str]) -> List[Dict]:
        """Crawl multiple news pages.
        
        Args:
            urls: List of URLs to crawl
            
        Returns:
            List of crawled articles
        """
        results = []
        
        for url in urls:
            try:
                article = await self.crawl_page(url)
                if article:
                    results.append(article)
                await asyncio.sleep(2)
            except Exception as e:
                logger.error(f"Failed to crawl {url}: {e}")
                
        return results
    
    def extract_article_content(self, html: str) -> Dict:
        """Extract article content from HTML.
        
        Args:
            html: HTML content
            
        Returns:
            Dictionary with extracted content
        """
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(html, 'lxml')
        
        article = {}
        
        title_elem = soup.find('h1') or soup.find('title')
        article['title'] = title_elem.get_text().strip() if title_elem else ''
        
        content_elem = soup.find('article') or soup.find('div', class_='content')
        if content_elem:
            article['content'] = content_elem.get_text(strip=True, separator=' ')
            
        return article


class ScrapySpider:
    """Scrapy-based spider for crawling news."""
    
    name = 'news_spider'
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.articles = []
        
    def parse(self, response):
        """Parse response and extract article data."""
        for article in response.css('article'):
            yield {
                'title': article.css('h2::text').get(),
                'url': article.css('a::attr(href)').get(),
                'crawled_at': datetime.now().isoformat()
            }
    
    async def crawl_async(self, url: str) -> Dict:
        """Async crawl method."""
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text()
                return self.extract_article_content(text)
    
    def extract_article_content(self, html: str) -> Dict:
        """Extract article content from HTML."""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(html, 'lxml')
        
        article = {}
        
        title_elem = soup.find('h1')
        article['title'] = title_elem.get_text().strip() if title_elem else ''
        
        content_elem = soup.find('article') or soup.find('div', class_=lambda x: x and 'content' in x)
        if content_elem:
            article['content'] = content_elem.get_text(strip=True, separator=' ')
            
        return article
