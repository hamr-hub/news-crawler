"""Search Engine Module - Discovers news websites via search engines."""

import requests
from typing import List, Dict, Optional
import logging
import time
import random

logger = logging.getLogger(__name__)


class SearchEngine:
    """Search engine for discovering news websites."""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
    def search(self, query: str, engine: str = 'google', max_results: int = 50) -> List[Dict]:
        """Search for news websites using the specified search engine.
        
        Args:
            query: Search query
            engine: Search engine name (google, baidu, yandex)
            max_results: Maximum number of results to return
            
        Returns:
            List of search results with url, title, snippet
        """
        results = []
        
        try:
            if engine == 'google':
                results = self._search_google(query, max_results)
            elif engine == 'baidu':
                results = self._search_baidu(query, max_results)
            elif engine == 'yandex':
                results = self._search_yandex(query, max_results)
            else:
                logger.warning(f"Unknown search engine: {engine}")
                
        except Exception as e:
            logger.error(f"Search error ({engine}): {e}")
            
        return results
    
    def _search_google(self, query: str, max_results: int) -> List[Dict]:
        """Search using Google."""
        results = []
        start = 0
        
        while len(results) < max_results:
            url = f"https://www.google.com/search"
            params = {
                'q': query,
                'num': min(10, max_results - len(results)),
                'start': start
            }
            
            try:
                response = self.session.get(url, params=params, timeout=10)
                response.raise_for_status()
                
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'lxml')
                
                for item in soup.select('div.g'):
                    link = item.select_one('a')
                    if link and link.get('href'):
                        url = link['href']
                        if url.startswith('http'):
                            title_elem = item.select_one('h3')
                            snippet_elem = item.select_one('div.VwiC3b')
                            
                            results.append({
                                'url': url,
                                'title': title_elem.get_text() if title_elem else '',
                                'snippet': snippet_elem.get_text() if snippet_elem else ''
                            })
                            
                start += 10
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                logger.error(f"Google search error: {e}")
                break
                
        return results[:max_results]
    
    def _search_baidu(self, query: str, max_results: int) -> List[Dict]:
        """Search using Baidu."""
        results = []
        pn = 0
        
        while len(results) < max_results:
            url = "https://www.baidu.com/s"
            params = {
                'wd': query,
                'pn': pn,
                'rn': min(10, max_results - len(results))
            }
            
            try:
                response = self.session.get(url, params=params, timeout=10)
                response.raise_for_status()
                
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'lxml')
                
                for item in soup.select('div.result'):
                    link = item.select_one('a')
                    if link and link.get('href'):
                        url = link['href']
                        title_elem = item.select_one('h3')
                        snippet_elem = item.select_one('div.c-abstract')
                        
                        results.append({
                            'url': url,
                            'title': title_elem.get_text() if title_elem else '',
                            'snippet': snippet_elem.get_text() if snippet_elem else ''
                        })
                        
                pn += 10
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                logger.error(f"Baidu search error: {e}")
                break
                
        return results[:max_results]
    
    def _search_yandex(self, query: str, max_results: int) -> List[Dict]:
        """Search using Yandex."""
        results = []
        page = 0
        
        while len(results) < max_results:
            url = "https://yandex.com/search/"
            params = {
                'text': query,
                'page': page,
                'numdoc': min(10, max_results - len(results))
            }
            
            try:
                response = self.session.get(url, params=params, timeout=10)
                response.raise_for_status()
                
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'lxml')
                
                for item in soup.select('div.serp-item'):
                    link = item.select_one('a.link')
                    if link and link.get('href'):
                        url = link['href']
                        title_elem = item.select_one('h2')
                        snippet_elem = item.select_one('div.text-container')
                        
                        results.append({
                            'url': url,
                            'title': title_elem.get_text() if title_elem else '',
                            'snippet': snippet_elem.get_text() if snippet_elem else ''
                        })
                        
                page += 1
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                logger.error(f"Yandex search error: {e}")
                break
                
        return results[:max_results]
    
    def discover_news_sites(self, max_per_engine: int = 20) -> List[Dict]:
        """Discover news websites from multiple search engines.
        
        Args:
            max_per_engine: Maximum results per search engine
            
        Returns:
            List of discovered news sites
        """
        news_sites = []
        queries = [
            "top news websites",
            "breaking news site:news",
            "latest headlines site:news",
            "world news site:com",
        ]
        
        for engine in ['google', 'baidu', 'yandex']:
            for query in queries:
                try:
                    results = self.search(query, engine=engine, max_results=max_per_engine)
                    for r in results:
                        r['engine'] = engine
                        news_sites.append(r)
                    time.sleep(2)
                except Exception as e:
                    logger.error(f"Error discovering sites from {engine}: {e}")
                    
        return news_sites
