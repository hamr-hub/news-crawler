"""GitHub Issue Handler - Automatically handles GitHub issues."""

import re
import logging
from typing import Dict, Optional, List
from datetime import datetime
import requests

logger = logging.getLogger(__name__)


class GitHubIssueHandler:
    """Handles GitHub issues for automatic bug fixing."""
    
    ISSUE_TYPE_PATTERNS = {
        'parsing': r'not.*(load|parse|extract)|selector.*(fail|error)|can\'t.*find',
        'network': r'timeout|connection|DNS|network.*error',
        'rate_limit': r'rate.*limit|429|too.*many.*request',
        'authentication': r'401|403|forbidden|unauthorized|login',
        'data': r'empty|missing.*data|no.*result',
    }
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.repo = self.config.get('repo', '')
        self.token = self.config.get('token', '')
        self.session = requests.Session()
        
        if self.token:
            self.session.headers.update({
                'Authorization': f'token {self.token}',
                'Accept': 'application/vnd.github.v3+json'
            })
            
    def parse_issue(self, issue_body: str) -> Dict:
        """Parse GitHub issue to extract relevant information.
        
        Args:
            issue_body: The issue body text
            
        Returns:
            Dictionary with parsed information
        """
        result = {
            'url': None,
            'error': None,
            'description': None,
            'issue_type': self.detect_issue_type(issue_body)
        }
        
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, issue_body)
        if urls:
            result['url'] = urls[0]
            
        error_patterns = [
            r'Error:?\s*(.+?)(?:\n|$)',
            r'Exception:?\s*(.+?)(?:\n|$)',
            r'(?:Timeout|Connection|Parse).*?error',
        ]
        
        for pattern in error_patterns:
            match = re.search(pattern, issue_body, re.IGNORECASE)
            if match:
                result['error'] = match.group(1).strip()
                break
                
        return result
    
    def detect_issue_type(self, issue_body: str) -> str:
        """Detect the type of issue.
        
        Args:
            issue_body: The issue body text
            
        Returns:
            Issue type string
        """
        for issue_type, pattern in self.ISSUE_TYPE_PATTERNS.items():
            if re.search(pattern, issue_body, re.IGNORECASE):
                return issue_type
                
        return 'unknown'
    
    def get_issues(self, state: str = 'open') -> List[Dict]:
        """Get GitHub issues.
        
        Args:
            state: Issue state (open, closed, all)
            
        Returns:
            List of issues
        """
        if not self.repo:
            logger.warning("GitHub repo not configured")
            return []
            
        url = f"https://api.github.com/repos/{self.repo}/issues"
        params = {'state': state}
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching issues: {e}")
            return []
    
    def create_issue(self, title: str, body: str) -> Optional[Dict]:
        """Create a new GitHub issue.
        
        Args:
            title: Issue title
            body: Issue body
            
        Returns:
            Created issue data or None
        """
        if not self.repo:
            return None
            
        url = f"https://api.github.com/repos/{self.repo}/issues"
        data = {'title': title, 'body': body}
        
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error creating issue: {e}")
            return None
    
    def close_issue(self, issue_number: int) -> bool:
        """Close a GitHub issue.
        
        Args:
            issue_number: Issue number
            
        Returns:
            True if successful
        """
        if not self.repo:
            return False
            
        url = f"https://api.github.com/repos/{self.repo}/issues/{issue_number}"
        data = {'state': 'closed'}
        
        try:
            response = self.session.patch(url, json=data)
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Error closing issue: {e}")
            return False
    
    def add_comment(self, issue_number: int, comment: str) -> bool:
        """Add a comment to an issue.
        
        Args:
            issue_number: Issue number
            comment: Comment text
            
        Returns:
            True if successful
        """
        if not self.repo:
            return False
            
        url = f"https://api.github.com/repos/{self.repo}/issues/{issue_number}/comments"
        data = {'body': comment}
        
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Error adding comment: {e}")
            return False
