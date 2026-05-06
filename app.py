import streamlit as st
import google.generativeai as genai
import pandas as pd
import feedparser
from PIL import Image

# 1. 網頁全域設置
st.set_page_config(page_title="TRADE AI - 多策略進化終端", layout="wide")

# --- 側邊欄：多策略配置 ---
with st.sidebar:
    st.title("🛡️ 交易核心配置")
    api_key = st.text_input("🔑 Gemini API Key:", type="password")
    
    st.divider()
    # 策略切換開關
    strategy_mode = st.selectbox(
        "選擇當前執行策略：",
        ["A. 5k 極限防守 (Funding Pips)", "B. 100k 機構獵殺 (Institutional)"]
    )
    
    st.divider()
    # 賬戶監控 (動態調整)
    if "5k" in strategy_mode:
        balance = st.number_input("當前 5k 帳戶餘額:", value=5000.0)
        st.warning(f"今日最大虧損限額: ${balance * 0.05:.2f}")
    else:
        balance = st.number_input("當前 100k 帳戶餘額:", value=100000.0)
        st.info(f"單筆 1% 風險建議: ${balance * 0.01:.2f}")

    st.divider()
    # 策略定義區 (根據選擇自動更新)
    if "5k" in strategy_mode:
        current_sop = "【邏輯】：H1順勢 + M5折扣區(0.618)動能反轉。止損減半機制。"
    else:
        current_sop = "【邏輯】：D1趨勢 + PDH/PDL 獵殺 + H4 影線 SFP + H1 MSS 結構破壞 + OB/Fibo 共振進場。"
    
    my_strategy = st.text_area("當前 SOP 核心：", value=current_sop, height=200)

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
        return f"AI 異常: {e}"

# --- 主頁面 ---
st.title(f"🏹 {strategy_mode} 決策與進化中心")

# 1. 5星預警 (雷達)
if api_key:
    if st.button("📡 掃描 5 星級核彈預警"):
        with st.spinner("正在排查全球宏觀噪音..."):
            feed = feedparser.parse("https://search.cnbc.com/rs/search/view.xml?partnerId=2000&keywords=macroeconomics&sort=date")
            raw_data = "\n\n".join([f"標題: {e.title} \n摘要: {e.summary}" for e in feed.entries[:15]])
            prompt = f"分析新聞：{raw_data}。只有影響力評分 >= 9 且對黃金/外匯有重磅衝擊的新聞才報告。否則回答 SAFE。"
            warning_res = get_ai_response(prompt, api_key)
            if warning_res and "SAFE" not in warning_res:
                st.error(f"🚨 5星預警：{warning_res}")
            else:
                st.success("✅ 市場環境目前無 5 星級威脅。")

st.divider()

# 2. 策略量化研究室
st.subheader("🔬 策略量化研究室")
uploaded_file = st.file_uploader("導入交易記錄 CSV (對應當前選中策略)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("📊 數據預覽：")
    st.dataframe(df.head(5), use_container_width=True)

    st.subheader("🧠 執行策略審計與模式識別")
    trade_context = st.text_area("補充此單/此階段的開倉心理或背景描述：")

    if st.button("🧪 執行深度進化分析") and api_key:
        with st.spinner("軍師正在比對當前 SOP 進行數據分析..."):
            data_str = df.to_string()
            prompt = f"""
            你是一名頂級量化分析師。請針對交易員正在使用的【策略 {strategy_mode}】進行審計。
            
            【SOP 規則】：{m
