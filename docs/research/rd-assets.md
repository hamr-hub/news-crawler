# 研发资产沉淀报告

## 1. 项目概况
- **项目类型**: Python 爬虫项目
- **核心框架**: Scrapy, Playwright
- **AI 能力**: OpenAI (站点分类、内容聚合、选择器自愈)

## 2. 核心架构
- `news_crawler/crawler/spiders/`: 爬虫实现 (发现爬虫, 新闻爬虫)
- `news_crawler/ai_modules/`: AI 集成模块 (site_classifier, news_aggregator, self_healing)
- `news_crawler/crawler/`: Scrapy 核心配置 (pipelines, items, settings, rules_manager)

## 3. 代码片段建议
- **Scrapy 爬虫模板**: `news_crawler/crawler/spiders/`
- **AI 模块调用**: `news_crawler/ai_modules/`
