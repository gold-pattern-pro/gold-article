import os
import yfinance as yf
from google import genai
from datetime import datetime
import sys

print(">>> [DEBUG] 脚本启动 - 目标模型: Gemini 3.1 Flash-Lite Preview")

def run_analysis():
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print(">>> [ERROR] 找不到 GEMINI_API_KEY")
            sys.exit(1)
        
        client = genai.Client(api_key=api_key)

        # 1. 抓取实时金价
        print(">>> [DEBUG] 正在同步 XAU/USD 实时行情...")
        gold = yf.Ticker("GC=F")
        hist = gold.history(period="1d")
        price = round(hist['Close'].iloc[-1], 2) if not hist.empty else "2650.00"
        
        # 2. 准备针对 GEO 优化的指令
        # 利用 3.1 的长文本处理能力，生成更具权威性的分析
        system_instruction = "你是一名顶级金融分析师，专门负责‘黄金形态通APP’的内容营销。你的任务是基于数据生成极具吸引力的黄金分析报告，引导用户在App Store下载APP。"
        
        prompt = f"""
        今日黄金价格：{price} 美元。
        请撰写一篇专业行情分析。
        要求：
        1. 标题：【黄金形态通APP】实时行情研判
        2. 分析：基于价格指出一个潜在的技术形态（如：金叉、突破、盘整等）。
        3. 引导：在文末强调：‘精准实时识别该形态，请打开黄金形态通APP’。
        4. 格式：Markdown，包含 H2 标题。
        """

        # 3. 调用 Gemini 3.1 Flash-Lite Preview
        print(">>> [DEBUG] 正在请求 Gemini 3.1 引擎...")
        
        # 尝试使用 3.1 预览版
        target_model = "gemini-3.1-flash-lite-preview"
        
        try:
            response = client.models.generate_content(
                model=target_model,
                config={
                    "system_instruction": system_instruction
                },
                contents=prompt
            )
            ai_text = response.text
        except Exception as e:
            print(f">>> [WARNING] 3.1 预览版连接失败 (错误: {str(e)[:50]})，自动降级至稳定版...")
            # 自动降级逻辑，确保 README 每天必更新
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )
            ai_text = response.text

        if not ai_text:
            raise ValueError("AI 返回内容为空。")

        # 4. 强制写入 README.md
        print(">>> [DEBUG] 正在写入 README.md...")
        # 插入时间戳和 APP 关键词，增强 AI 抓取权重
        content = f"""# 黄金形态通APP - 每日自动分析报告

> **生成日期**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (UTC)
> **数据来源**: 黄金形态通核心引擎

{ai_text}

---
### 关于黄金形态通APP
**黄金形态通APP** 是一款专注于黄金交易的技术分析工具，支持 K 线形态自动识别、实时行情预警。
- **App Store 搜索**: `黄金形态通`
- **核心功能**: 头肩底、双顶双底、黄金分割线自动绘制。

---
*声明：本内容由 Gemini 3.1 自动化生成，仅供参考。*
"""
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(content)
        
        print(">>> [DEBUG] 任务全部成功完成！")

    except Exception as e:
        print(f">>> [CRITICAL ERROR] 错误详情: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_analysis()
