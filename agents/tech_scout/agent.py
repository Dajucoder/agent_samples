import os
import feedparser
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# ==========================================
# 0. 网络与代理配置 (访问 Reddit/OpenAI 必需)
# ==========================================
# 请根据你的实际情况修改端口号 (Clash通常是7890)
# 如果你在服务器环境或已经全局代理，可注释掉这两行
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

# ==========================================
# 1. 定义 RSS 数据源库
# ==========================================

# 1.1 用户定义的高质量源
RSS_SOURCES = [
    {
        "keys": ["hf", "huggingface", "hugging face"],
        "name": "Hugging Face 博客",
        "url": "https://huggingface.co/blog/feed.xml",
        "desc": "包含最新的AI模型和技术发布"
    },
    {
        "keys": ["reddit", "reddit ml", "机器学习"],
        "name": "Reddit MachineLearning",
        "url": "https://www.reddit.com/r/MachineLearning/.rss",
        "desc": "Reddit机器学习社区热门讨论"
    },
    {
        "keys": ["mit", "tech review", "科技评论"],
        "name": "MIT Tech Review",
        "url": "https://www.technologyreview.com/feed/",
        "desc": "MIT科技评论科技新闻"
    },
    {
        "keys": ["openai", "oa"],
        "name": "OpenAI 博客",
        "url": "https://openai.com/blog/rss.xml",
        "desc": "OpenAI官方博客"
    },
    {
        "keys": ["deepmind", "google ai"],
        "name": "DeepMind 博客",
        # 修正了 DeepMind 最新的 RSS 地址，旧地址可能失效
        "url": "https://deepmind.google/blog/rss/index.xml", 
        "desc": "DeepMind/Google DeepMind 官方博客"
    },
    # 保留之前的中文优质源，做个混合双打
    {
        "keys": ["36kr", "36氪"],
        "name": "36氪",
        "url": "https://36kr.com/feed",
        "desc": "中国商业科技新闻"
    },
    {
        "keys": ["qbit", "量子位"],
        "name": "量子位",
        "url": "https://www.qbitai.com/feed",
        "desc": "中文 AI 垂直媒体"
    }
]

# ==========================================
# 2. 定义工具
# ==========================================

def rss_reader_tool(query: str) -> str:
    """
    根据关键词或 URL 获取 RSS 订阅源的最新内容。
    
    Args:
        query: 媒体名称关键词（如 "OpenAI", "Reddit", "36kr"）或直接的 URL。
    """
    query = query.lower().strip()
    target_url = None
    source_name = "未知来源"

    print(f"\n[Tool] 用户查询 RSS: {query} ...")

    # --- 1. 智能匹配逻辑 ---
    # 如果输入的是 http 开头的，直接用
    if query.startswith("http"):
        target_url = query
        source_name = "自定义URL"
    else:
        # 遍历我们的源列表进行模糊匹配
        for source in RSS_SOURCES:
            # 检查 keys 列表或 name 字段
            if query in source["keys"] or query in source["name"].lower():
                target_url = source["url"]
                source_name = source["name"]
                print(f"[Tool] 命中预设源: {source_name}")
                break
        
        # 如果没匹配到，做一个默认回落（Optional）
        if not target_url:
            if "ai" in query or "模型" in query:
                # 默认看 Hugging Face
                target_url = "https://huggingface.co/blog/feed.xml"
                source_name = "Hugging Face (自动推荐)"
            else:
                available_keys = ", ".join([s["name"] for s in RSS_SOURCES])
                return f"未找到匹配的源。支持的源包括：{available_keys}。或者请直接提供 URL。"

    # --- 2. 解析逻辑 ---
    try:
        # 增加 timeout 防止卡死
        # agent 这里的 User-Agent 很重要，有些网站（如 Reddit）会拦截默认 UA
        feed = feedparser.parse(
            target_url, 
            agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)"
        )
        
        if feed.bozo and feed.bozo_exception:
            print(f"[Tool Warning] 解析由错误但尝试继续: {feed.bozo_exception}")

        if not feed.entries:
            return f"成功连接到 {source_name}，但没有发现文章内容（可能是反爬虫拦截或源为空）。"

        # --- 3. 格式化输出 ---
        entries_data = []
        # 获取前 5 篇即可，Reddit 内容可能很长
        for entry in feed.entries[:5]:
            title = entry.get("title", "无标题")
            link = entry.get("link", "")
            # 处理摘要：移除多余 HTML 标签，截断
            summary = entry.get("summary", entry.get("description", ""))
            # 简单的清洗 HTML 标签 (也可引入 BeautifulSoup，这里用简单切片代替)
            summary_clean = summary.replace("<p>", "").replace("</p>", "").replace("<br>", "\n")[:250]
            
            entries_data.append(f"📌 {title}\n🔗 {link}\n📝 {summary_clean}...")
            
        result_text = f"【来源：{source_name}】\n最新文章列表：\n" + "\n\n".join(entries_data)
        return result_text

    except Exception as e:
        return f"读取 RSS 失败 ({source_name}): {str(e)}\n请检查网络连通性或代理设置。"

# ==========================================
# 3. 配置 LiteLLM
# ==========================================
# 确保 .env 文件配置正确
api_base = os.environ.get("IFLOW_API_BASE")
api_key = os.environ.get("IFLOW_API_KEY")
model_name = os.environ.get("MODELNAME") # 确保这个模型存在

os.environ["OPENAI_API_BASE"] = api_base
os.environ["OPENAI_API_KEY"] = api_key

custom_model = LiteLlm(
    model=f"openai/{model_name}",
    temperature=0.3
)

# ==========================================
# 4. Agent 定义
# ==========================================

# 动态生成支持列表字符串，放入 Prompt 中，这样 LLM 就知道它能查什么
source_list_str = "\n".join([f"- {s['name']}: {s['desc']}" for s in RSS_SOURCES])

instruction = f"""
你是一个【全球前沿科技情报官】，专注于 AI 和科技领域的趋势分析。
你的核心能力是通过 RSS 工具读取最新的博客和新闻。

【支持的权威数据源】：
{source_list_str}

【工作流程】：
1. 当用户询问某个特定机构（如 OpenAI, DeepMind）或话题（如 "Reddit 上在讨论什么"）时，调用 `rss_reader_tool`。
2. 即使即使用户没有明确说名字，比如问“最近 AI 有什么突破”，你也应该主动去查阅 Hugging Face 或 MIT Tech Review。
3. **输出要求**：
   - 先列出你查阅了哪些源。
   - 对获取的文章进行**总结**，不要只是罗列标题。
   - 提取出**核心洞察**（Key Insights）。
   - 如果是英文源，请将核心内容**翻译为中文**输出。
   - 给出每个文章的访问地址。

请保持专业、客观、敏锐。
"""

root_agent = Agent(
    name="tech_scout",
    model=custom_model,
    instruction=instruction,
    tools=[rss_reader_tool]
)