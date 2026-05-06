import streamlit as st
import google.generativeai as genai
import pandas as pd
from PIL import Image
import feedparser # 新增：用於抓取新聞流

# 網頁設置
st.set_page_config(page_title="TRADE AI - 職業交易終端", layout="wide")

# --- 側邊欄：導航與核心配置 ---
with st.sidebar:
    st.title("🛡️ TRADE AI 終端")
    api_key = st.text_input("🔑 輸入 Gemini API Key:", type="password")
    st.divider()
    menu = st.radio("工作區切換：", ["🌅 每日晨報：隔夜大事", "📡 實時作戰：基本面與劇本", "🔬 週末研究：策略實驗室"])
    st.divider()
    st.subheader("📜 核心 SOP (Funding Pips 5k)")
    default_sop = "【環境】：H1 ATR > 5 | 【結構】：H1 同色K線 -> Fibo | 【進場】：M5 0.618 + 吞沒 | 【防禦】：0.5R止損減半"
    st.caption(default_sop)

# --- AI 初始化函數 ---
def get_ai_response(prompt, key):
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model.generate_content(prompt).text
    except Exception as e:
        return f"AI 服務異常: {e}"

# --- 功能函數：自動抓取宏觀新聞 ---
def fetch_macro_news():
    # 使用 CNBC 的財經宏觀 RSS 源（免費且穩定）
    rss_url = "https://search.cnbc.com/rs/search/view.xml?partnerId=2000&keywords=macroeconomics&sort=date&minimumrelevance=0.2&pubtime=30&pubfreq=h&categories=exclude"
    feed = feedparser.parse(rss_url)
    news_list = []
    for entry in feed.entries[:15]: # 抓取最新的 15 條
        news_list.append(f"標題: {entry.title} \n摘要: {entry.summary}")
    return "\n\n".join(news_list)

# --- 模塊一：🌅 每日晨報（自動抓取與解讀） ---
if menu == "🌅 每日晨報：隔夜大事":
    st.title("🌅 隔夜宏觀早報")
    st.write("點擊下方按鈕，AI 將自動掃描全球宏觀資訊，並針對黃金交易進行篩選。")
    
    if st.button("🚀 獲取今日晨報") and api_key:
        with st.spinner("正在掃描全球資訊並進行邏輯過濾..."):
            # 1. 抓取原始新聞
            raw_news_data = fetch_macro_news()
            
            # 2. 讓 AI 進行過濾和總結
            prompt = f"""
            你是一名頂級宏觀策略分析師。請閱讀以下過去 24 小時的全球財經新聞：
            {raw_news_data}
            
            任務：
            1. 【噪音過濾】：刪除所有與美元(USD)、黃金(XAU)、通脹、利率、地緣政治無關的新聞。
            2. 【大事清單】：用列表總結最重要的 3-5 件事。
            3. 【影響權重】：每件事標註影響力 (1-10分) 以及利多/利空黃金。
            4. 【操作定調】：今早開機，針對 Funding Pips 5k 賬戶，給出一個總體基調（例如：今日宜守不宜攻、今日動能強勁等）。
            請用簡練的中文回答。
            """
            report = get_ai_response(prompt, api_key)
            st.markdown("---")
            st.success("✅ 今日晨報已生成：")
            st.markdown(report)
    elif not api_key:
        st.warning("👈 請先輸入 API Key")

# --- 模塊二：📡 實時作戰（保持原有功能） ---
elif menu == "📡 實時作戰：基本面與劇本":
    st.title("📡 實時作戰決策中心")
    # ... (此處保留之前的快訊分析和劇本代碼) ...
    st.subheader("📰 基本面快訊分析")
    news_input = st.text_area("粘贴金十快訊：")
    if st.button("分析方向") and api_key:
        st.info(get_ai_response(f"分析此消息對黃金影響及SOP符合度：{news_input}", api_key))
    
    st.subheader("🎭 劇本預演")
    event = st.text_input("即將公布數據")
    if st.button("生成劇本") and api_key:
        st.write(get_ai_response(f"數據{event}即將公布，給出三種走勢劇本。", api_key))

# --- 模塊三：🔬 策略實驗室（保持原有功能） ---
else:
    st.title("🔬 策略量化研究室")
    uploaded_file = st.file_uploader("導入歷史數據 CSV", type="csv")
    if uploaded_file and api_key:
        df = pd.read_csv(uploaded_file)
        if st.button("🧪 開始量化分析"):
            data_str = df.to_string()
            prompt = f"分析這些交易數據，尋找隱藏規律：{data_str}"
            st.markdown(get_ai_response(prompt, api_key))
