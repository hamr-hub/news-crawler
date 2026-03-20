import uuid
import hashlib

def generate_text_hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def aggregate_news(title, content):
    """
    简化的新闻聚合逻辑。
    在实际生产环境中，应当使用向量数据库（如 Qdrant / Milvus）将文本转为 Embedding 后进行相似度搜索。
    由于没有本地运行的向量数据库实例，这里使用基于内容的简单哈希或UUID来模拟事件ID的生成。
    """
    if not title and not content:
        return str(uuid.uuid4())
        
    text = f"{title}. {content}"[:500]
    
    # 模拟：将前500个字符作为指纹，实际应替换为向量搜索或 SimHash
    event_id = generate_text_hash(text)
    
    return f"event_{event_id[:16]}"
