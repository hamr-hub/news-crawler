import json
import logging
from openai import OpenAI

# 假设使用 OpenAI 的模型进行标定，也可以换成其他开源模型
client = OpenAI()

def classify_site(domain, html_snippet):
    """
    使用大模型对站点进行自动归类、标定国家和新闻类型
    """
    prompt = f"""
    Please analyze the following HTML snippet of a news website (Domain: {domain}) and determine:
    1. The likely country of origin (ISO 3166-1 alpha-2 format, e.g., 'US', 'CN').
    2. The primary language (ISO 639-1 format, e.g., 'en', 'zh').
    3. The primary news category (e.g., 'general', 'finance', 'sports', 'technology').

    HTML Snippet:
    {html_snippet[:4000]}  # 截取部分以节省 token

    Respond strictly in JSON format:
    {{
        "country": "...",
        "language": "...",
        "category": "..."
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        result = json.loads(response.choices[0].message.content)
        logging.info(f"Classified {domain}: {result}")
        return result
    except Exception as e:
        logging.error(f"Failed to classify site {domain}: {e}")
        return {"country": "unknown", "language": "unknown", "category": "unknown"}
