import json
import logging
from openai import OpenAI
from crawler.crawler.rules_manager import update_rules

# 初始化 OpenAI 客户端 (需要环境变量 OPENAI_API_KEY)
client = OpenAI()

def heal_rules(domain, html_content, old_rules):
    """
    当爬虫原有的提取规则失效时，调用大模型分析当前页面的 HTML，
    自动生成并返回新的 CSS 选择器或 XPath 规则，以实现爬虫的自愈。
    """
    logging.info(f"Initiating self-healing for domain: {domain}")
    
    # 截断 HTML 避免超过 token 限制 (这里为了演示简单截断，实际可以使用 BeautifulSoup 移除 <script> 等无关标签)
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    for script in soup(["script", "style", "nav", "footer", "iframe"]):
        script.decompose()
    clean_html = soup.get_text(separator=' ', strip=True)[:8000] # 取清理后的前 8000 字符，或者直接传结构化 HTML
    
    # 也可以直接传递 HTML 片段，这里传递稍微清洗过的 HTML 以提高大模型理解效率
    html_snippet = str(soup.body)[:8000] if soup.body else html_content[:8000]

    prompt = f"""
    You are an expert web scraping AI. The existing CSS/XPath rules for the news domain '{domain}' have stopped working because the website structure has changed.
    
    Old Rules that failed: 
    {json.dumps(old_rules, indent=2)}
    
    Your task is to analyze the provided HTML snippet and deduce the NEW CSS selectors needed to successfully extract the news articles.
    
    Required fields to extract and their expected typical selectors:
    1. 'list_selector': The selector for the list of article cards/containers on the page. (e.g., '.article-list .item', 'article')
    2. 'url_selector': The selector to get the href link from within an article card. (e.g., 'a.title-link::attr(href)')
    3. 'title_selector': The selector to get the main title on the article detail page. (e.g., 'h1.main-title::text')
    4. 'content_selector': The selector to get the article body paragraphs. (e.g., '.article-body p::text')
    5. 'time_selector': The selector to get the publication time. (e.g., 'time::attr(datetime)')
    
    Please return ONLY a valid JSON object with the keys 'list_selector', 'url_selector', 'title_selector', 'content_selector', and 'time_selector' mapped to their new working CSS selectors. Do not include any explanation text.

    HTML Snippet:
    ```html
    {html_snippet}
    ```
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106", # 或者使用更强大的模型如 gpt-4
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" },
            temperature=0.2
        )
        
        content = response.choices[0].message.content
        new_rules = json.loads(content)
        
        # 验证新规则是否包含所需键
        required_keys = ['list_selector', 'url_selector', 'title_selector', 'content_selector']
        if all(k in new_rules for k in required_keys):
            # 将新规则持久化到 Redis 或其他配置中心
            update_rules(domain, new_rules)
            logging.info(f"Successfully healed rules for {domain}. New rules: {new_rules}")
            return new_rules
        else:
            logging.error(f"Healed rules are missing required keys. Received: {new_rules}")
            return None
            
    except Exception as e:
        logging.error(f"Failed to heal rules via AI for {domain}: {e}")
        return None
