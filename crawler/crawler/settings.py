BOT_NAME = 'news_crawler'

SPIDER_MODULES = ['crawler.crawler.spiders']
NEWSPIDER_MODULE = 'crawler.crawler.spiders'

# Scrapy-Playwright settings
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Playwright config
PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,
}

# Redis settings (for distributed crawling)
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
REDIS_URL = 'redis://localhost:6379'

# Pipelines
ITEM_PIPELINES = {
    'crawler.crawler.pipelines.AIAggregationPipeline': 300,
    'crawler.crawler.pipelines.JsonWriterPipeline': 400,
}

# AI Settings (Replace with actual)
OPENAI_API_KEY = "your-api-key"
QDRANT_URL = "localhost"

ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 16
