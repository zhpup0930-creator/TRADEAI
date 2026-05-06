import streamlit as st
import google.generativeai as genai
import pandas as pd
from PIL import Image
import feedparser

# 1. 網頁設置
st.set_page_config(page_title="TRADE AI - 終極交易終端", layout="wide")

# --- 側邊欄：導航與核心配置 ---
with st.sidebar:
    st.title("🛡️ TRADE AI 終端")
    api_key = st.text_input("🔑 輸入 Gemini API Key:", type="password")
    
    st.divider()
    menu = st.radio(
        "切換工作區：",
        ["🌅 每日晨報：隔夜大事", "📡 實時作戰：基本面與劇本", "🔬 週末研究：策略實驗室"]
    )
    
    st.divider()
    st.subheader("📜 核心 SOP (Funding Pips 5k)")
    default_sop = """
    【環境】：H1 ATR(14) > 5
    【結構】：H1 連續2根同色K線 -> 拉 Fibo
    【進場】：M5 回撤至 0.618-1.0 + 吞沒K線
    【防禦】：盈虧比 1:1；0.5R時止損手動減半
    【強平】：週五 23:30 強制平倉
    """
    my_strategy = st.text_area("當前 SOP 規則：", value=default_sop, height=200)

# --- AI 核心函數 (自動匹配可用模型，徹底解決404) ---
def get_ai_response(prompt, key):
    if not key:
        return "👈 請先在左側輸入 API Key 以啟動系統。"
    try:
        genai.configure(api_key=key)
        # 自動搜尋可用模型
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name.replace('models/', ''))
        
        if not available_models:
            return "❌ 你的 API Key 暫無可用模型權限。"
        
        # 選擇最強模型 (優先選 flash，其次選 pro)
        best_model = "gemini-1.5-flash" if "gemini-1.5-flash" in available_models else available_models[0]
        model = genai.GenerativeModel(best_model)
        
        # 發送請求
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI 服務異常: {e}"

# --- 功能：自動抓取 CNBC 宏觀新聞源 ---
def fetch_macro_news():
    try:
        rss_url = "https://search.cnbc.com/rs/search/view.xml?partnerId=2000&keywords=macroeconomics&sort=date"
        feed = feedparser.parse(rss_url)
        news_list = []
        for entry in feed.entries[:10]: # 抓取最新的 10 條
            news_list.append(f"標題: {entry.title} \n摘要: {entry.summary}")
        return "\n\n".join(news_list)
    except:
        return "無法獲取新聞流，請手動粘贴消息進行分析。"

# --- 模塊一：🌅 每日晨報 ---
if menu == "🌅 每日晨報：隔夜大事":
    st.title("🌅 隔夜宏觀早報")
    st.write("點擊按鈕，AI 將自動掃描全球宏觀資訊並過濾黃金(XAUUSD)相關大事。")
    
    if st.button("🚀 獲取今日晨報"):
        with st.spinner("軍師正在翻閱全球財經報紙..."):
            raw_news_data = fetch_macro_news()
            prompt = f"""
            你是一名頂級分析師。請分析過去24小時的新聞：
            {raw_news_data}
            
            任務：
            1. 總結最重要的 3 條黃金/美元相關大事。
            2. 給出每件事的影響分 (1-10分)。
            3. 根據我的 SOP ({my_strategy})，給出今日交易的總體心態建議。
            用大白話總結。
            """
            st.markdown("---")
            st.success("✅ 今日晨報已生成：")
            st.markdown(get_ai_response(prompt, api_key))

# --- 模塊二：📡 實時作戰 --
