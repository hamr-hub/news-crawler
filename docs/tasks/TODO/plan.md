# 新闻爬虫系统 - 开发任务清单

## 项目信息

- **平台**: Python
- **技术栈**: Scrapy + Playwright
- **测试覆盖率目标**: 80%
- **单任务最少测试数**: 3

## P0 任务

### 测试任务

| ID | 任务 | 测试类型 | 文件 |
|----|------|----------|------|
| T0-1 | 项目基础结构测试 | pure | crawler/tests/test_config.py |
| T0-2 | 搜索引擎模块测试 | pure | crawler/tests/test_search_engine.py |
| T0-3 | 网站分类模块测试 | pure | crawler/tests/test_site_classifier.py |
| T0-4 | 去重服务测试 | pure | crawler/tests/test_deduplicator.py |
| T0-5 | 存储服务测试 | pure | crawler/tests/test_storage.py |

### 代码任务

| ID | 任务 | 依赖 | 文件 |
|----|------|------|------|
| P0-1 | 创建项目基础配置和目录结构 | - | requirements.txt, config.yaml |
| P0-2 | 实现搜索引擎模块 | T0-2 | crawler/services/search_engine.py |
| P0-3 | 实现网站分类模块 | T0-3 | crawler/services/site_classifier.py |
| P0-4 | 实现新闻爬取 Worker | P0-3 | crawler/workers/news_spider.py |
| P0-5 | 实现去重服务 | T0-4 | crawler/services/deduplicator.py |
| P0-6 | 实现 JSON 存储服务 | T0-5, P0-4 | crawler/services/storage.py |
| P0-7 | 实现爬虫启动入口 | P0-6 | crawler/start_crawl.py |

## P1 任务

### 测试任务

| ID | 任务 | 测试类型 | 文件 |
|----|------|----------|------|
| T1-1 | AI 修复模块测试 | pure | crawler/tests/test_ai_repair.py |
| T1-2 | GitHub Issue 处理模块测试 | pure | crawler/tests/test_github_issue_handler.py |

### 代码任务

| ID | 任务 | 依赖 | 文件 |
|----|------|------|------|
| P1-1 | 实现 AI 修复模块 | T1-1 | crawler/services/ai_repair.py |
| P1-2 | 实现 GitHub Issue 处理模块 | T1-2 | crawler/services/github_issue_handler.py |

## 执行命令

```bash
# 运行测试
pytest crawler/tests/ -v

# 代码检查
flake8 crawler/ --max-line-length=120
```

## 验收标准

- 所有 P0 测试通过
- 代码符合 PEP 8 规范
- 支持完整爬取流程

## 回滚预案

- 回滚配置文件
- 删除新增模块
