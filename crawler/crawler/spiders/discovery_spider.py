import scrapy
import urllib.parse
from ai_modules.site_classifier import classify_site
import redis
import json

class DiscoverySpider(scrapy.Spider):
    name = "discovery_spider"
    
    def __init__(self, *args, **kwargs):
        super(DiscoverySpider, self).__init__(*args, **kwargs)
        # 连接本地 Redis 用于存储发现的站点信息
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        # 预设一些搜索引擎查询入口
        self.search_engines = [
            "https://www.google.com/search?q=latest+news",
            # "https://www.bing.com/search?q=新闻"
        ]

    def start_requests(self):
        for url in self.search_engines:
            # 对于搜索引擎结果页，使用 Playwright 处理可能存在的动态加载和反爬
            yield scrapy.Request(url, meta={'playwright': True}, callback=self.parse_search_results)

    def parse_search_results(self, response):
        # 提取搜索结果中的链接 (这是一个简单的示例提取规则，实际中不同搜索引擎的选择器不同)
        links = response.css('a::attr(href)').getall()
        for link in links:
            if link.startswith('http'):
                domain = urllib.parse.urlparse(link).netloc
                # 如果这个域名还没有被记录，就去访问它的首页进行标定
                if not self.redis_client.sismember('discovered_domains', domain):
                    # 避免访问明显不是新闻网站的链接，这里可以加黑名单过滤
                    if "google.com" not in domain and "bing.com" not in domain:
                        yield scrapy.Request(
                            f"http://{domain}",
                            meta={'domain': domain, 'playwright': True},
                            callback=self.parse_and_classify_site
                        )

    def parse_and_classify_site(self, response):
        domain = response.meta['domain']
        
        # 提取页面部分内容用于 LLM 标定
        html_snippet = response.text[:5000]
        
        # 调用 AI 模块进行站点标定
        classification = classify_site(domain, html_snippet)
        
        site_info = {
            "url": response.url,
            "domain": domain,
            "classification": classification
        }
        
        # 将标定后的站点信息存入 Redis
        self.redis_client.hset('sites_info', domain, json.dumps(site_info))
        self.redis_client.sadd('discovered_domains', domain)
        
        self.logger.info(f"Discovered and classified site: {domain} -> {classification}")
        yield site_info
