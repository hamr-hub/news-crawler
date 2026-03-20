import scrapy
from crawler.items import NewsItem
from crawler.rules_manager import get_rules
from ai_modules.self_healing import heal_rules
import urllib.parse
import redis
import json

class NewsSpider(scrapy.Spider):
    name = "news_spider"
    
    def __init__(self, *args, **kwargs):
        super(NewsSpider, self).__init__(*args, **kwargs)
        # 连接 Redis 获取需要爬取的站点
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

    def start_requests(self):
        # 从 Redis 获取所有已发现和标定的站点
        sites = self.redis_client.hgetall('sites_info')
        if not sites:
            self.logger.warning("No sites found in Redis 'sites_info'. Using fallback start_urls.")
            fallback_urls = ['https://news.ycombinator.com/']
            for url in fallback_urls:
                domain = urllib.parse.urlparse(url).netloc
                yield scrapy.Request(
                    url, 
                    meta={'playwright': True, 'domain': domain, 'classification': {}},
                    callback=self.parse
                )
            return

        for domain, site_data_json in sites.items():
            site_data = json.loads(site_data_json)
            url = site_data.get('url')
            classification = site_data.get('classification', {})
            if url:
                yield scrapy.Request(
                    url, 
                    meta={'playwright': True, 'domain': domain, 'classification': classification},
                    callback=self.parse,
                    dont_filter=True # 首页需要反复爬取以发现新内容
                )

    def parse(self, response):
        domain = response.meta['domain']
        rules = get_rules(domain)
        
        # 使用动态规则提取新闻列表
        articles = response.css(rules.get('list_selector', 'article'))
        
        # 如果提取不到列表，触发自愈
        if not articles and response.status == 200:
            self.logger.warning(f"No articles found for {domain} with selector '{rules.get('list_selector')}'. Triggering self-healing...")
            new_rules = heal_rules(domain, response.text, rules)
            if new_rules:
                # 尝试用新规则再次提取
                articles = response.css(new_rules.get('list_selector', 'article'))
            else:
                self.logger.error(f"Self-healing failed for {domain}")
                return

        for article in articles:
            url_selector = rules.get('url_selector', 'a::attr(href)')
            url = article.css(url_selector).get()
            if url:
                url = response.urljoin(url)
                # 使用 Scrapy-Redis 的指纹过滤机制，如果 URL 已爬过，会自动被过滤
                yield scrapy.Request(
                    url, 
                    meta={
                        'playwright': True, 
                        'domain': domain, 
                        'rules': rules,
                        'classification': response.meta['classification']
                    },
                    callback=self.parse_detail
                )

    def parse_detail(self, response):
        rules = response.meta['rules']
        item = NewsItem()
        item['url'] = response.url
        item['site_domain'] = response.meta['domain']
        
        # 提取字段
        item['title'] = response.css(rules.get('title_selector', 'h1::text')).get()
        contents = response.css(rules.get('content_selector', 'p::text')).getall()
        item['content'] = ' '.join(contents).strip()
        item['published_at'] = response.css(rules.get('time_selector', 'time::attr(datetime)')).get()
        
        # 填充标定信息
        classification = response.meta.get('classification', {})
        item['country'] = classification.get('country')
        item['news_type'] = classification.get('category')
        item['language'] = classification.get('language')
        
        if item['title'] and item['content']:
            yield item
