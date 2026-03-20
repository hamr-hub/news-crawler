"""News Deduplication Service - Removes duplicate news articles."""

from typing import List, Dict
from difflib import SequenceMatcher
import logging

logger = logging.getLogger(__name__)


class Deduplicator:
    """Deduplicates news articles based on content similarity."""
    
    def __init__(self, similarity_threshold: float = 0.85):
        self.similarity_threshold = similarity_threshold
        
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score between 0 and 1
        """
        if not text1 or not text2:
            return 0.0
            
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def is_duplicate(self, news1: Dict, news2: Dict, compare_title: bool = True, 
                     compare_content: bool = True) -> bool:
        """Check if two news items are duplicates.
        
        Args:
            news1: First news item
            news2: Second news item
            compare_title: Whether to compare titles
            compare_content: Whether to compare content
            
        Returns:
            True if items are duplicates
        """
        scores = []
        
        if compare_title and news1.get('title') and news2.get('title'):
            title_sim = self.calculate_similarity(
                news1['title'], 
                news2['title']
            )
            scores.append(title_sim)
            
        if compare_content and news1.get('content') and news2.get('content'):
            content_sim = self.calculate_similarity(
                news1['content'],
                news2['content']
            )
            scores.append(content_sim)
            
        if not scores:
            return False
            
        max_score = max(scores)
        return max_score >= self.similarity_threshold
    
    def deduplicate(self, news_list: List[Dict]) -> List[Dict]:
        """Remove duplicate news items.
        
        Args:
            news_list: List of news items
            
        Returns:
            Deduplicated list of news items
        """
        if not news_list:
            return []
            
        unique_news = []
        
        for news in news_list:
            is_dup = False
            
            for existing in unique_news:
                if self.is_duplicate(news, existing):
                    is_dup = True
                    
                    if news.get('crawled_at') and existing.get('crawled_at'):
                        if news['crawled_at'] > existing['crawled_at']:
                            unique_news[unique_news.index(existing)] = news
                            
                    break
                    
            if not is_dup:
                unique_news.append(news)
                
        logger.info(f"Deduplicated {len(news_list)} -> {len(unique_news)} news items")
        return unique_news
    
    def find_similar(self, news_item: Dict, news_list: List[Dict], 
                     limit: int = 5) -> List[Dict]:
        """Find similar news items.
        
        Args:
            news_item: Reference news item
            news_list: List to search in
            limit: Maximum number of results
            
        Returns:
            List of similar news items with similarity scores
        """
        similar = []
        
        for news in news_list:
            if news.get('id') == news_item.get('id'):
                continue
                
            similarity = self.calculate_similarity(
                news_item.get('title', ''),
                news.get('title', '')
            )
            
            if similarity >= self.similarity_threshold:
                similar.append({
                    'news': news,
                    'similarity': similarity
                })
                
        similar.sort(key=lambda x: x['similarity'], reverse=True)
        return similar[:limit]
