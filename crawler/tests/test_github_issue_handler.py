import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def test_github_handler_import():
    from crawler.services.github_issue_handler import GitHubIssueHandler
    assert GitHubIssueHandler is not None


def test_github_handler_init():
    from crawler.services.github_issue_handler import GitHubIssueHandler
    handler = GitHubIssueHandler()
    assert handler is not None


def test_parse_issue():
    from crawler.services.github_issue_handler import GitHubIssueHandler
    handler = GitHubIssueHandler()
    
    issue_body = """
    ## Issue
    Crawler failed to fetch https://example.com
    
    ## Error
    TimeoutError: Connection timeout
    
    ## Expected
    Should fetch the page successfully
    """
    
    parsed = handler.parse_issue(issue_body)
    assert parsed is not None
    assert 'url' in parsed or 'error' in parsed


def test_issue_type_detection():
    from crawler.services.github_issue_handler import GitHubIssueHandler
    handler = GitHubIssueHandler()
    
    issue_bodies = [
        ("Website not loading", "parsing"),
        ("Connection timeout", "network"),
        ("Rate limit exceeded", "rate_limit"),
    ]
    
    for body, expected_type in issue_bodies:
        issue_type = handler.detect_issue_type(body)
        assert issue_type is not None
