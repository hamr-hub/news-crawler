import json
import redis

# Use Redis to store rules so they can be updated dynamically
redis_client = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)

DEFAULT_RULES = {
    "list_selector": "article",
    "url_selector": "a::attr(href)",
    "title_selector": "h1::text, h2::text",
    "content_selector": ".article-content p::text, .story-body p::text",
    "time_selector": "time::attr(datetime)"
}

def get_rules(domain):
    rules = redis_client.get(f"rules:{domain}")
    if rules:
        return json.loads(rules)
    return DEFAULT_RULES

def update_rules(domain, new_rules):
    redis_client.set(f"rules:{domain}", json.dumps(new_rules))
