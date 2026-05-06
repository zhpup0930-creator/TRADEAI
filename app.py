import streamlit as st
import google.generativeai as genai
import pandas as pd
import feedparser
from PIL import Image

# 1. 網頁全域設置 (單頁寬屏)
st.set_page_config(page_title="TRADE AI - 策略進化終端", layout="wide")

# --- 側邊欄：核心配置 (憲法區) ---
with st.sidebar:
    st.title("🛡️ 交易憲法")
    api_key = st.text_input("🔑 Gemini API Key:", type="password")
    st.divider()
    st.subheader("📜 核心 SOP")
    default_sop = "【環境】：H1 ATR > 5 | 【結構】：H1 同色K線 -> Fibo | 【進場】：M5 0.618 + 吞沒 | 【防禦】：0.5R止損減半"
    my_strategy = st.text_area("當前 SOP 定義：", value=default_sop, height=300)
    st.info("AI 將嚴格以此規則作為審計與進化的唯一準則。")

# --- AI 核心函數 (自動匹配) ---
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

# --- 功能：新聞掃描 ---
def fetch_news():
    rss_url = "https://search.cnbc.com/rs/search/view.xml?partnerId=2000&keywords=macroeconomics&sort=date"
    feed = feedparser.parse(rss_url)
    return "\n\n".join([f"標題: {e.title} \n摘要: {e.summary}" for e in feed.entries[:15]])

# --- 主頁面開始 ---

# A. 頂部：5星級核彈雷達 (只有點擊且有大事才會出現紅色大框)
st.title("🛡️ 策略進化與風險監控中心")

if api_key:
    if st.button("📡 掃描 5 星級核彈預警"):
        with st.spinner("正在排查全球噪音..."):
            raw_data = fetch_news()
            # 強制 AI 只在有 9 分以上事件時才說話
            prompt = f"""
            你是一名冷酷的風險控制官。
            分析以下新聞：{raw_data}
            
            規則：
            1. 只有影響力打分 >= 9 的新聞才允許報告。
            2. 如果有，請用「大標題 + 影響邏輯 + 操作禁令」的格式回答。
            3. 如果沒有 9 分以上的事件，請【精確】回答「SAFE」這四個字母，不要說任何廢話。
            """
            warning_res = get_ai_response(prompt, api_key)
            
            if warning_res and "SAFE" not in warning_res:
                st.error("🚨🚨🚨 偵測到 5 星級核彈事件！🚨🚨🚨")
                st.markdown(f"### {warning_res}")
            else:
                st.success("✅ 目前市場無 5 星級威脅，請專注於你的 SOP 執行。")

st.divider()

# B. 中部：策略量化研究室 (你的核心工作區)
st.subheader("🔬 策略量化研究室")
st.write("上傳 CSV 歷史數據，找出盈虧背後的隱藏共性。")

c1, c2 = st.columns([1, 2])
with c1:
    uploaded_file = st.file_uploader("導入 CSV 交易流水", type="csv")
    additional_context = st.text_area("補充你的主觀感悟：", placeholder="這兩周心態如何？市場有什麼特殊情況？")

with c2:
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("📊 待分析數據預覽：")
        st.dataframe(df.head(10), use_container_width=True)

if st.button("🧪 執行深度量化模式識別"):
    if not api_key:
        st.warning("👈 請先輸入 API Key")
    elif not uploaded_file:
        st.warning("請先上傳 CSV 文件")
    else:
        with st.spinner("正在進行大數據相關性分析..."):
            data_str = df.to_string()
            prompt = f"""
            你是一名量化數據科學家。
            【我的 SOP】：{my_strategy}
            【交易記錄數據】：{data_str}
            【主觀背景】：{additional_context}
            
            任務：
            1. 【隱藏共性】：找出虧損單中除了 SOP 之外的共同環境特徵（時間、ATR、美元狀態、DXY等）。
            2. 【盈虧同源分析】：盈利單具備哪些 SOP 沒寫但共同存在的細節？
            3. 【策略進化】：針對 Funding Pips 5k 帳戶的低回撤要求，給出 2 條具體的進化建議。
            """
            analysis_res = get_ai_response(prompt, api_key)
            st.markdown("---")
            st.success("🔬 策略研究報告已生成：")
            st.markdown(analysis_res)

# 頁腳
st.divider()
st.caption("TRADE AI | 專注策略進化 | 5星風險過濾")
