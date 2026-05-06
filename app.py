import streamlit as st
import google.generativeai as genai
import pandas as pd
import feedparser
from PIL import Image

# 1. 網頁全域設置
st.set_page_config(page_title="TRADE AI - 終極進化終端", layout="wide")

# --- 側邊欄：核心配置與賬戶健康監控 ---
with st.sidebar:
    st.title("🛡️ 交易核心配置")
    api_key = st.text_input("🔑 Gemini API Key:", type="password")
    
    st.divider()
    # 賬戶健康度監控 (針對 Funding Pips 5k 帳戶)
    st.subheader("💰 賬戶健康度")
    curr_balance = st.number_input("當前餘額 (Current Balance):", value=5000.0)
    # Funding Pips 5k 的每日 5% 風險限額計算
    daily_drawdown_limit = curr_balance * 0.05
    total_drawdown_limit = 5000 * 0.10 # 初始資金的 10%
    
    st.metric(label="今日最大回撤限額 (5%)", value=f"${daily_drawdown_limit:.2f}")
    st.metric(label="帳戶總爆倉線 (10%)", value=f"${5000 - total_drawdown_limit:.2f}")
    
    st.divider()
    st.subheader("📜 核心 SOP 規則")
    default_sop = "【環境】：H1 ATR > 5 | 【結構】：H1 同色K線 -> Fibo | 【進場】：M5 0.618 + 吞沒 | 【防禦】：0.5R止損減半"
    my_strategy = st.text_area("SOP 定義：", value=default_sop, height=200)

# --- AI 核心函數 ---
def get_ai_response(prompt, key):
    if not key: return None
    try:
        genai.configure(api_key=key)
        available_models = [m.name.replace('models/', '') for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        best_model = "gemini-1.5-flash" if "gemini-1.5-flash" in available_models else available_models[0]
        model = genai.GenerativeModel(best_model)
        return model.generate_content(prompt).text
    except Exception as e:
        return f"AI 服務異常: {e}"

# --- 功能：5星新聞抓取 ---
def fetch_news():
    try:
        rss_url = "https://search.cnbc.com/rs/search/view.xml?partnerId=2000&keywords=macroeconomics&sort=date"
        feed = feedparser.parse(rss_url)
        return "\n\n".join([f"標題: {e.title} \n摘要: {e.summary}" for e in feed.entries[:15]])
    except:
        return "無法獲取新聞流。"

# --- 主頁面 ---

# A. 頂部：5星級核彈雷達 (僅顯示 9 分以上消息)
st.title("🛡️ 策略進化與風險監控中心")

if api_key:
    if st.button("📡 掃描 5 星級核彈預警"):
        with st.spinner("正在排查全球宏觀噪音..."):
            raw_data = fetch_news()
            prompt = f"分析以下新聞：{raw_data}。規則：只有影響力評分 >= 9 的新聞才報告。如果沒有，請精確回答 SAFE。如果有，請給出警告和操作禁令。"
            warning_res = get_ai_response(prompt, api_key)
            
            if warning_res and "SAFE" not in warning_res:
                st.error(f"🚨🚨🚨 偵測到 5 星級核彈事件：\n\n{warning_res}")
            else:
                st.success("✅ 目前市場環境無 5 星級威脅，請專注於 SOP 執行。")

st.divider()

# B. 中部：策略量化研究室 (含數據視覺化)
st.subheader("🔬 策略量化研究室")
st.write("上傳你的 CSV 交易歷史，AI 將找出肉眼看不見的隱藏規律。")

uploaded_file = st.file_uploader("導入交易記錄 CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # --- 數據視覺化展示 ---
    st.subheader("📊 策略執行統計")
    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        # 如果 CSV 裡有 Result (TP/SL/Half-SL) 這一列，自動畫圖
        if 'Result' in df.columns:
            st.write("勝率分佈圖 (TP vs SL)")
            res_chart = df['Result'].value_counts()
            st.bar_chart(res_chart)
        else:
            st.info("提示：如果在 CSV 增加 'Result' 列，此處可顯示勝率圖表。")
            
    with col_v2:
        st.write("核心數據摘要")
        st.dataframe(df.describe())

    st.divider()
    
    # --- AI 深度分析 ---
    st.subheader("🧠 執行深度量化分析")
    context = st.text_area("補充最近的心得或盤感：")
    
    if st.button("🧪 啟動 AI 模式識別"):
        if not api_key:
            st.warning("👈 請先輸入 API Key")
        else:
            with st.spinner("軍師正在分析數據相關性..."):
                data_str = df.to_string()
                prompt = f"""
                你是一名量化數據分析師。
                【我的 SOP】：{my_strategy}
                【交易記錄數據】：{data_str}
                【主觀背景】：{context}
                
                任務：
                1. 找出虧損單中除了 SOP 之外的共同環境特徵。
                2. 分析 MAEx，判斷止損緩衝是否合理。
                3. 給出 2 條具體的進化建議，以適應 Funding Pips 5k 帳戶。
                """
                analysis_res = get_ai_response(prompt, api_key)
                st.success("🔬 策略研究報告已生成：")
                st.markdown(analysis_res)

# 頁腳
st.divider()
st.caption("TRADE AI | 數據驅動 | 絕對理性 | 專為 Funding Pips 5k 設計")
