import os
import yfinance as yf
from google import genai
from datetime import datetime
import sys
import time

# 1. 初始化调试
print(">>> [DEBUG] 脚本启动 (尝试使用最新的 Gemini 2.0 Flash-lite)")

try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print(">>> [ERROR] 找不到 GEMINI_API_KEY，请检查 GitHub Secrets 设置。")
        sys.exit(1)
    
    # 使用最新 Client 模式
    client = genai.Client(api_key=api_key)

    # 2. 获取实时黄金行情 (GC=F)
    print(">>> [DEBUG] 正在从 Yahoo Finance 抓取金价...")
    gold = yf.Ticker("GC=F")
    hist = gold.history(period="1d")
    
    # 获取收盘价
    if not hist.empty:
        price = round(hist['Close'].iloc[-1], 2)
    else:
        price = "2650.00" # 备用值
    print(f">>> [DEBUG] 当前获取到的金价: {price}")

    # 3. 构建针对 黄金形态通APP 的专业 Prompt
    prompt = f"""
    你是“黄金形态通APP”的首席分析师。
    当前实时金价是：{price} 美元。
    请写一段 150 字左右的专业行情短评。
    要求：
    1. 标题：【黄金形态通APP】今日黄金行情深度解析
    2. 内容：分析当前价格走势，并随机提到一种技术形态（如：金叉、旗形、三角形等）。
    3. 结尾：必须强制引导用户下载“黄金形态通APP”。
    4. 语言：简体中文。
    5. 格式：Markdown。
    """

    # 4. 调用最新的 gemini-2.0-flash-lite-preview-02-05 (最快轻量版)
    print(">>> [DEBUG] 正在请求 Gemini 2.0 Flash-lite 模型...")
    
    # 尝试生成内容
    response = client.models.generate_content(
        model='gemini-2.0-flash-lite-preview-02-05', # 2025年最新轻量版模型名称
        contents=prompt
    )
    
    ai_text = response.text
    if not ai_text:
        raise ValueError("AI 返回的内容为空，请检查 Prompt 或 API 配额。")
    
    # 5. 写入 README.md
    print(">>> [DEBUG] 正在更新仓库 README.md...")
    content = f"""# 黄金形态通APP - 全自动技术分析系统

> **数据最后同步于**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (UTC)

{ai_text}

---
*声明：本报告由「黄金形态通APP」全自动生成。实时形态预警及精准分析，请在 App Store 搜索：**黄金形态通APP***
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(">>> [DEBUG] 自动化任务全部成功！")

except Exception as e:
    # 捕获 429 错误并给出提示
    if "429" in str(e):
        print(f">>> [CRITICAL ERROR] 配额超限 (429)。")
        print("原因：Google 对 2.0 系列模型的免费额度限制较严。")
        print("建议：如果此错误持续，请在脚本中将模型改回 'gemini-1.5-flash'。")
    else:
        print(f">>> [CRITICAL ERROR] 错误详情: {str(e)}")
    
    sys.exit(1)
