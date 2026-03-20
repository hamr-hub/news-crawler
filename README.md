# News Crawler

AI-powered news crawler with auto-repair and GitHub integration.

## Features

- **Auto-discovery**: Discover news sites via search engines, auto-classify by country/type
- **Continuous crawling**: Run scheduled news crawling with deduplication
- **AI repair**: Auto-fix crawler errors using OpenAI
- **GitHub integration**: Auto-create issues for failed crawls, QCoder auto-fix

## Requirements

- Python 3.10+
- Redis (optional, for production)

## Installation

```bash
pip install -r requirements.txt
playwright install
```

## Configuration

Create `.env` file or set environment variables:

```bash
export GITHUB_TOKEN="your_github_token"
export OPENAI_API_KEY="your_openai_api_key"
```

Edit `config.yaml` to customize settings.

## Usage

```bash
python crawler/start_crawl.py
```

## Testing

```bash
python -m pytest crawler/tests/ -v
```

## Project Structure

```
crawler/
├── services/          # Core services
│   ├── search_engine.py
│   ├── site_classifier.py
│   ├── deduplicator.py
│   ├── storage.py
│   ├── ai_repair.py
│   └── github_issue_handler.py
├── workers/           # Spider workers
│   └── news_spider.py
├── tests/             # Unit tests
└── start_crawl.py     # Entry point
```

## License

MIT
