# 新闻聚合爬虫系统文档 (News Aggregation Crawler System)

## 1. 需求文档 (PRD)

### 1.1 项目背景
为了构建一个全面的全球新闻聚合平台，需要开发一套高可用、智能化的分布式爬虫系统。该系统能够自动发现新闻源、智能分类、持续采集最新新闻，并具备自我修复和自动化运维能力。

### 1.2 核心功能需求
1. **智能站点发现与标定**：
   - 自动通过主流搜索引擎（Google, Baidu, Yandex等）搜索新闻网站。
   - 使用NLP/大模型对发现的站点进行自动归类，标定其所属国家、语言及新闻类型（如综合、科技、财经、体育等）。
2. **增量与聚合爬取**：
   - 核心框架使用 Scrapy + Playwright（处理动态渲染页面）。
   - 循环采集已知新闻源，通过去重机制（URL、标题或内容哈希）确保每次只爬取最新内容。
   - 实现新闻事件聚合：在同一时间窗口内，将不同站点报道的“相同内容/事件”的新闻进行汇总和关联。
   - 数据统一保存为 JSON 格式。
3. **AI自动修复爬虫 (Self-Healing)**：
   - 捕获爬取过程中的异常（如选择器失效、DOM结构改变、反爬验证等）。
   - 异常发生时，将报错信息及当前页面DOM快照发送给AI模型进行校对。
   - 自动生成新的提取规则或Playwright脚本代码，并在隔离环境中测试，测试通过后热更新至运行中的爬虫。
4. **自动化运维与开源管理**：
   - 项目代码托管于 GitHub。
   - 集成 Qcoder（或类似AI编码助手）监听 GitHub Issues。
   - 当用户提出 Issue（如某个站点报错或增加新需求）时，自动触发 Qcoder 进行代码修复，并提交 PR。

---

## 2. 技术实现路径

### 2.1 爬虫核心框架
- **Scrapy**: 作为基础调度、并发请求管理、数据管道（Pipeline）处理的核心框架。
- **Scrapy-Playwright**: 结合 Scrapy，用于处理需要JS渲染、复杂反爬或需模拟交互的新闻页面。
- **存储**: 使用 Scrapy 的 `JsonItemExporter` 或自定义 Pipeline，将清洗后的结构化数据（标题、正文、时间、作者、来源、归类等）写入 JSON 文件或 JSON-line 格式。

### 2.2 站点发现与标定
- **搜索引擎接口**: 爬取或调用 Search API（Google Custom Search, Baidu API, Yandex XML API）。
- **标定引擎**: 将获取到的站点 Meta 信息和少量页面文本输入给 LLM（如 GPT-4 / Claude / 开源模型）。要求 LLM 返回标准化的 JSON，包含 `{"country": "CN", "type": "finance", "language": "zh"}`。

### 2.3 新闻聚合与增量采集
- **增量爬取**: 引入 Redis/布隆过滤器（Bloom Filter）或 Scrapy-DeltaFetch，利用 URL 或内容摘要进行指纹判重。
- **内容聚合**: 
  - 提取新闻核心要素（时间+实体提取/Embedding向量化）。
  - 利用向量数据库（如 Milvus, Qdrant）或基于 TF-IDF/SimHash 的近线算法，计算相似度，将同一时间段相似度大于设定阈值的新闻合并为同一个 Event。

### 2.4 AI自动修复 (Self-Healing)
- **监控模块**: 封装 Scrapy Spider 的 `errback` 及解析异常（如 `extract` 返回空）。
- **校对与生成**: 获取当前页面的 HTML/截图，连同报错日志，调用大模型 API（Prompt: "该页面的标题结构已变更，请根据提供的HTML提供新的XPath或CSS选择器"）。
- **热更新**: 将大模型返回的规则存储到数据库（如 Redis, MongoDB），爬虫从数据库动态加载 XPath/CSS 选择器，而不是硬编码在源文件中。

### 2.5 自动化 Issue 修复
- 利用 GitHub Actions 和 Webhooks 监听 `issues` 事件。
- 触发 Qcoder Agent，读取 Issue 描述，拉取代码库，执行修改，运行单元测试。
- 自动向主分支提交 Pull Request，通过后自动合并（CI/CD 流水线）。

---

## 3. 系统架构设计

### 3.1 架构图说明
系统分为五大模块：**发现层**、**采集层**、**处理层**、**自愈层**、**持续集成层**。

```text
[搜索引擎 API/爬虫] 
       ↓ 
[发现层 (Site Discovery)] ---> [LLM 标定服务] ---> (站点资源库 Database)
                                                    ↓
(调度队列 Redis) <------------------------ [Scrapy Master 节点]
       ↓                                            ↓
[采集层 (Scrapy + Playwright Worker 节点 1..N)] <--- (动态规则中心)
       ↓
[处理层 (数据清洗、布隆去重、SimHash/向量聚合)]
       ↓
[存储层 (JSON / JSONL 文件存储系统 / 分布式存储 HDFS/S3)]
       
====================== 辅助系统 =======================
[自愈层 (Self-Healing Monitor)] 
   |-> 监听解析错误 -> 抓取 DOM -> LLM 生成新规则 -> 更新(动态规则中心)

[持续集成层 (GitHub + Qcoder)]
   |-> 监听 Issue -> Qcoder Agent 分析修复 -> 提交 PR -> 触发 CI/CD
```

---

## 4. 核心实现文档 (代码参考结构)

### 4.1 目录结构
```text
news-crawler/
├── scrapy.cfg
├── setup.py
├── requirements.txt
├── .github/
│   └── workflows/
│       └── qcoder_auto_fix.yml   # 监听 Issue 自动修复流水线
├── crawler/
│   ├── __init__.py
│   ├── items.py                  # 定义 NewsItem
│   ├── middlewares.py            # 代理、Playwright 中间件
│   ├── pipelines.py              # JSON 导出、增量去重、AI 聚合
│   ├── settings.py               # Redis、Playwright 配置
│   ├── rules_manager.py          # 动态从 Redis 读取提取规则
│   └── spiders/
│       ├── discovery_spider.py   # 搜索引擎发现爬虫
│       └── news_spider.py        # 通用新闻爬虫 (基于动态规则)
├── ai_modules/
│   ├── site_classifier.py        # 调用 LLM 标定站点
│   ├── self_healing.py           # 异常修复脚本 (分析 DOM 返回规则)
│   └── news_aggregator.py        # 内容相似度比对与聚合逻辑
└── scripts/
    └── run_cluster.sh            # 分布式启动脚本
```

### 4.2 核心代码片段示例

**1. Scrapy+Playwright 新闻爬虫 (news_spider.py)**
```python
import scrapy
from crawler.items import NewsItem
from crawler.rules_manager import get_rules

class DynamicNewsSpider(scrapy.Spider):
    name = "news_spider"
    
    def start_requests(self):
        for site in self.get_sites_from_db():
            yield scrapy.Request(
                site['url'], 
                meta={'playwright': True, 'site_info': site},
                callback=self.parse
            )

    def parse(self, response):
        site_info = response.meta['site_info']
        rules = get_rules(site_info['domain']) # 动态获取解析规则
        
        items = response.css(rules['list_selector'])
        if not items:
            # 触发 AI 自愈机制
            self.trigger_self_healing(site_info['domain'], response.text)
            return

        for item in items:
            url = item.css(rules['url_selector']).get()
            if self.is_new(url): # 增量判断
                yield scrapy.Request(url, callback=self.parse_detail, meta=response.meta)
```

**2. 数据写入 JSON (pipelines.py)**
```python
import json

class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open('news_output.jsonl', 'a', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "
"
        self.file.write(line)
        return item
```

---

## 5. 分布式部署文档

### 5.1 环境依赖
- **操作系统**: Ubuntu 20.04+ 或 CentOS 8+
- **环境**: Python 3.9+, Node.js (Playwright 依赖), Docker & Docker Compose
- **中间件**: Redis (用于分布式请求队列和去重), Qdrant/Milvus (可选，用于新闻聚合向量比对)

### 5.2 分布式架构部署
项目采用 **Scrapy-Redis** 实现多节点分布式抓取。

**1. 中间件部署 (Redis)**
```bash
docker run -d --name redis-server -p 6379:6379 redis:alpine
```

**2. 爬虫节点部署 (Worker)**
编写 `Dockerfile`：
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN playwright install --with-deps chromium
COPY . .
CMD ["scrapy", "crawl", "news_spider"]
```

**3. 启动集群**
在多台服务器上运行 Worker 节点，连接到同一个 Redis 实例：
```bash
# settings.py 中配置 REDIS_URL = 'redis://<master_ip>:6379/0'
docker build -t news-crawler .
docker run -d --name crawler-worker-1 news-crawler
docker run -d --name crawler-worker-2 news-crawler
```

### 5.3 自动化运维配置 (GitHub + Qcoder)
1. 在项目仓库中创建 `.github/workflows/qcoder.yml`。
2. 配置当 `issues` 开启时，运行 Qcoder CLI 脚本。
3. 提供相关 API 密钥（如 OpenAI Key, GitHub Token）至 GitHub Secrets。
4. **Issue 流程**：用户提交 "NYTimes 提取报错" -> Action 触发 Qcoder -> Qcoder 分析 Issue、修改 `rules_manager` 或对应Spider -> Qcoder 提交 PR -> 管理员合并 -> CI/CD 自动触发 Worker 节点拉取新代码重启。
