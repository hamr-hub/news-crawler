"""News Storage Service - Saves news data to JSON files."""

import json
import os
from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class NewsStorage:
    """Stores news data in JSON format."""
    
    def __init__(self, base_dir: str = "data/news"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
    def _get_date_path(self, date: Optional[str] = None) -> Path:
        """Get the directory path for a specific date."""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
            
        date_dir = self.base_dir / date
        date_dir.mkdir(parents=True, exist_ok=True)
        return date_dir
    
    def _get_filename(self, source: str) -> str:
        """Generate filename based on source."""
        safe_source = source.lower().replace(' ', '_').replace('/', '_')
        return f"{safe_source}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    def to_json(self, data: Dict) -> str:
        """Convert data to JSON string.
        
        Args:
            data: Data to serialize
            
        Returns:
            JSON string
        """
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    def save_news(self, news_data: Dict, date: Optional[str] = None) -> bool:
        """Save a single news item.
        
        Args:
            news_data: News data dictionary
            date: Optional date string (YYYY-MM-DD)
            
        Returns:
            True if successful
        """
        try:
            date_path = self._get_date_path(date)
            filename = self._get_filename(news_data.get('source', 'unknown'))
            filepath = date_path / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(news_data, f, ensure_ascii=False, indent=2)
                
            logger.info(f"Saved news to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving news: {e}")
            return False
    
    def save_news_batch(self, news_list: List[Dict], date: Optional[str] = None) -> bool:
        """Save multiple news items.
        
        Args:
            news_list: List of news data dictionaries
            date: Optional date string
            
        Returns:
            True if all successful
        """
        if not news_list:
            return True
            
        try:
            date_path = self._get_date_path(date)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filepath = date_path / f"batch_{timestamp}.json"
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(news_list, f, ensure_ascii=False, indent=2)
                
            logger.info(f"Saved {len(news_list)} news items to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving batch: {e}")
            return False
    
    def load_news(self, date: Optional[str] = None) -> List[Dict]:
        """Load news for a specific date.
        
        Args:
            date: Date string (YYYY-MM-DD), defaults to today
            
        Returns:
            List of news items
        """
        try:
            date_path = self._get_date_path(date)
            news_list = []
            
            for filepath in date_path.glob('*.json'):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            news_list.extend(data)
                        else:
                            news_list.append(data)
                except Exception as e:
                    logger.error(f"Error reading {filepath}: {e}")
                    
            return news_list
            
        except Exception as e:
            logger.error(f"Error loading news: {e}")
            return []
    
    def list_dates(self) -> List[str]:
        """List all dates with stored news.
        
        Returns:
            List of date strings
        """
        dates = []
        for d in self.base_dir.iterdir():
            if d.is_dir():
                dates.append(d.name)
        return sorted(dates, reverse=True)
    
    def get_stats(self) -> Dict:
        """Get storage statistics.
        
        Returns:
            Dictionary with stats
        """
        total_files = 0
        total_size = 0
        dates = self.list_dates()
        
        for date in dates:
            date_path = self.base_dir / date
            for f in date_path.glob('*.json'):
                total_files += 1
                total_size += f.stat().st_size
                
        return {
            'total_dates': len(dates),
            'total_files': total_files,
            'total_size_mb': round(total_size / (1024 * 1024), 2)
        }
