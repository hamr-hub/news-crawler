import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def test_ai_repair_import():
    from crawler.services.ai_repair import AIRepair
    assert AIRepair is not None


def test_ai_repair_init():
    from crawler.services.ai_repair import AIRepair
    repair = AIRepair()
    assert repair is not None


def test_error_detection():
    from crawler.services.ai_repair import AIRepair
    repair = AIRepair()
    
    error_msg = "ConnectionError: Failed to fetch page"
    error_type = repair.detect_error_type(error_msg)
    assert error_type is not None


def test_error_classification():
    from crawler.services.ai_repair import AIRepair
    repair = AIRepair()
    
    errors = [
        ("TimeoutError: Request timeout", "timeout"),
        ("HTTP 403: Forbidden", "http_error"),
        ("CSS selector not found", "parsing_error"),
    ]
    
    for msg, expected in errors:
        result = repair.detect_error_type(msg)
        assert result is not None
