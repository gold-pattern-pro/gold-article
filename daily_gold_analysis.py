import os
import yfinance as yf
import google.generativeai as genai
from datetime import datetime
import sys

# 1. 强制打印调试信息
print(">>> [DEBUG] 脚本启动...")

try:
    # 2. 检查 API Key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print(">>> [ERROR] 找不到 GEMINI_API_KEY，请检查 GitHub Secrets！")
        sys.exit(1)
    
    # 3. 尝试抓取金价
    print(">>> [DEBUG] 正在抓取金价数据...")
    gold = yf.Ticker("GC=F")
    hist = gold.history(period="1d")
    if hist.empty:
        # 如果 yfinance 抓不到，我们手动设一个价格防止脚本崩溃
        price = 2650.0
        print(">>> [WARNING] 无法实时抓取金价，使用模拟价格。")
    else:
        price = hist['Close'].iloc[-1]
    print(f">>> [DEBUG] 当前金价: {price}")

    # 4. 配置并调用 Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"请为黄金形态通APP写一篇黄金行情简评。当前金价{price}。要求：包含标题‘今日黄金走势分析’，字数100字左右。Markdown格式。"
    
    print(">>> [DEBUG] 正在请求 Gemini AI...")
    response = model.generate_content(prompt)
    ai_text = response.text
    print(f">>> [DEBUG] AI 返回内容长度: {len(ai_text)}")

    # 5. 强制写入文件（加入时间戳确保文件一定会被修改）
    print(">>> [DEBUG] 正在写入 README.md...")
    content = f"""# 黄金形态通APP - 每日更新
    
**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{ai_text}

---
*实时黄金形态分析，请在 App Store 搜索：黄金形态通APP*
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(">>> [DEBUG] 写入完成！")

except Exception as e:
    print(f">>> [CRITICAL ERROR] 发生严重错误: {str(e)}")
    sys.exit(1)
