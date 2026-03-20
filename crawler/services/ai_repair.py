"""AI Repair Module - Automatically fixes crawler errors using AI."""

import logging
import re
from typing import Dict, Optional, List
from openai import OpenAI

logger = logging.getLogger(__name__)


class AIRepair:
    """AI-powered error detection and repair for crawler."""
    
    ERROR_PATTERNS = {
        'timeout': r'timeout|TIMEOUT|Connection.*timeout|Read.*timeout',
        'http_error': r'HTTP\s*\d{3}|403|404|500|502|503',
        'parsing_error': r'selector|CSS|xpath|parse.*error',
        'authentication': r'401|Forbidden|Unauthorized|login',
        'rate_limit': r'rate.*limit|429|Too.*many.*requests',
        'network': r'ConnectionError|NetworkError|DNS',
        'javascript': r'JavaScript.*error|Playwright.*error',
    }
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.client = None
        self.max_retries = self.config.get('max_retries', 3)
        
        api_key = self.config.get('api_key')
        if api_key:
            self.client = OpenAI(api_key=api_key)
            
    def detect_error_type(self, error_message: str) -> Optional[str]:
        """Detect the type of error from error message.
        
        Args:
            error_message: The error message to analyze
            
        Returns:
            Error type string or None
        """
        for error_type, pattern in self.ERROR_PATTERNS.items():
            if re.search(pattern, error_message, re.IGNORECASE):
                return error_type
                
        return 'unknown'
    
    def analyze_error(self, error_message: str, context: Optional[str] = None) -> Dict:
        """Analyze error and generate fix suggestions.
        
        Args:
            error_message: The error message
            context: Additional context about the error
            
        Returns:
            Dictionary with analysis and suggestions
        """
        error_type = self.detect_error_type(error_message)
        
        analysis = {
            'error_type': error_type,
            'error_message': error_message,
            'suggestions': [],
            'fix_code': None
        }
        
        fix_strategies = {
            'timeout': [
                'Increase timeout value',
                'Add retry with exponential backoff',
                'Check network connection'
            ],
            'http_error': [
                'Check if URL is still valid',
                'Add proper headers',
                'Handle HTTP errors gracefully'
            ],
            'parsing_error': [
                'Update CSS selector',
                'Check page structure changes',
                'Add fallback selectors'
            ],
            'authentication': [
                'Update credentials',
                'Check session expiry'
            ],
            'rate_limit': [
                'Add rate limiting',
                'Use proxy rotation',
                'Add delay between requests'
            ],
            'network': [
                'Check DNS resolution',
                'Verify network connectivity',
                'Use retry mechanism'
            ],
            'javascript': [
                'Wait for page to fully load',
                'Check Playwright version',
                'Add explicit waits'
            ],
        }
        
        analysis['suggestions'] = fix_strategies.get(error_type, ['Unknown error type'])
        
        return analysis
    
    def generate_fix(self, error_message: str, file_path: str, 
                     function_name: str) -> Optional[str]:
        """Generate fix code using AI.
        
        Args:
            error_message: The error message
            file_path: Path to the file with error
            function_name: Function to fix
            
        Returns:
            Generated fix code or None
        """
        if not self.client:
            logger.warning("OpenAI client not configured")
            return None
            
        try:
            response = self.client.chat.completions.create(
                model=self.config.get('model', 'gpt-4'),
                messages=[
                    {
                        "role": "system",
                        "content": "You are a Python expert. Fix the crawler error and provide the corrected code."
                    },
                    {
                        "role": "user",
                        "content": f"Fix this error in {file_path}, function {function_name}:\n\nError: {error_message}\n\nProvide only the fixed code."
                    }
                ],
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating fix: {e}")
            return None
    
    def auto_repair(self, error: Exception, file_path: str, 
                    function_name: str) -> Dict:
        """Automatically repair an error.
        
        Args:
            error: The exception that occurred
            file_path: File with the error
            function_name: Function to fix
            
        Returns:
            Repair result dictionary
        """
        error_message = str(error)
        analysis = self.analyze_error(error_message)
        
        fix_code = None
        if self.client:
            fix_code = self.generate_fix(error_message, file_path, function_name)
            
        return {
            'success': fix_code is not None,
            'error_type': analysis['error_type'],
            'suggestions': analysis['suggestions'],
            'fix_code': fix_code
        }
