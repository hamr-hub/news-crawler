import json
from crawler.ai_modules.news_aggregator import aggregate_news

class AIAggregationPipeline:
    def process_item(self, item, spider):
        # Trigger AI aggregation to assign event_id based on similarity
        event_id = aggregate_news(item['title'], item['content'])
        item['event_id'] = event_id
        return item

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
