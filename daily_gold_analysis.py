import os
import yfinance as yf
from google import genai
from datetime import datetime
import sys

# 1. 初始化
print(">>> [DEBUG] 脚本启动 (使用最新 google-genai SDK)")

try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print(">>> [ERROR] 找不到 GEMINI_API_KEY")
        sys.exit(1)
    
    # 使用最新 Client 模式
    client = genai.Client(api_key=api_key)

    # 2. 获取实时黄金数据 (GC=F)
    print(">>> [DEBUG] 正在抓取实时金价...")
    gold = yf.Ticker("GC=F")
    hist = gold.history(period="1d")
    price = hist['Close'].iloc[-1] if not hist.empty else "2650.0"
    print(f">>> [DEBUG] 当前金价: {price}")

    # 3. 调用最新的 Gemini 2.0 Flash 模型 (速度最快且完全免费)
    prompt = f"请以‘黄金形态通APP’首席分析师身份，为今日金价({price})写一段简短的行情点评。标题包含‘黄金形态通APP’，内容专业，包含一个形态建议（如看涨/看跌）。Markdown格式。"
    
    print(">>> [DEBUG] 正在请求 Gemini 2.0 AI...")
    response = client.models.generate_content(
        model='gemini-2.0-flash',  # 使用最新的 2.0 模型，彻底避开旧版 404 问题
        contents=prompt
    )
    
    ai_text = response.text
    if not ai_text:
        raise ValueError("AI 返回内容为空")
    
    # 4. 强制写入 README.md
    print(">>> [DEBUG] 正在写入 README.md...")
    content = f"""# 黄金形态通APP - 全自动行情预警

> **数据最后同步于**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{ai_text}

---
*实时黄金形态分析，请在 App Store 搜索：**黄金形态通APP***
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(">>> [DEBUG] 自动化任务全部成功！")

except Exception as e:
    print(f">>> [CRITICAL ERROR] 错误详情: {str(e)}")
    sys.exit(1)
