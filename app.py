import streamlit as st
import google.generativeai as genai
import pandas as pd
from PIL import Image
import io

# 1. 網頁全域設置
st.set_page_config(page_title="TRADE AI - 終極交易終端", layout="wide")

# --- 側邊欄：導航與核心配置 ---
with st.sidebar:
    st.title("🛡️ TRADE AI 終端")
    api_key = st.text_input("🔑 輸入 Gemini API Key:", type="password")
    
    st.divider()
    # 導航菜單
    menu = st.radio(
        "切換工作區：",
        ["📡 實時作戰：基本面與劇本", "🔬 週末研究：策略進化實驗室"]
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
    st.info("AI 將在所有模式下以此 SOP 為核心進行分析。")

# --- AI 初始化函數 ---
def get_ai_response(prompt, key):
    if not key:
        st.warning("👈 請先輸入 API Key")
        return None
    try:
        genai.configure(api_key=key)
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target_model = "gemini-1.5-flash" if "models/gemini-1.5-flash" in models else models[0].replace('models/', '')
        model = genai.GenerativeModel(target_model)
        return model.generate_content(prompt).text
    except Exception as e:
        st.error(f"AI 連接失敗: {e}")
        return None

# --- 模塊一：📡 實時作戰（基本面、紅綠燈、劇本） ---
if menu == "📡 實時作戰：基本面與劇本":
    st.title("📡 實時作戰決策中心")
    
    # A. 數據防爆倉紅綠燈
    st.subheader("🚨 數據風險監控")
    col_red, col_info = st.columns([1, 4])
    with col_red:
        risk_level = st.selectbox("今日行情風險等級", ["🟢 低風險 (震盪)", "🟡 中風險 (有數據)", "🔴 高風險 (非農/CPI)"])
    with col_info:
        if "🔴" in risk_level:
            st.error("警告：今日有核彈級數據！數據公布前30分鐘必須清空 Funding Pips 倉位，嚴禁賭博。")
        else:
            st.success("環境相對穩定，請嚴格執行 SOP 畫線。")

    st.divider()

    # B. 金十新聞分析 (大白話翻譯機)
    st.subheader("📰 基本面大白話解讀")
    raw_news = st.text_area("粘贴金十快訊或你不懂的宏觀新聞：", height=150)
    if st.button("🚀 AI 翻譯並判斷方向"):
        with st.spinner("軍師正在分析 macro 邏輯..."):
            prompt = f"""
            你是一名頂級外匯分析師。請分析這段新聞：
            1. 給出影響評分 (1-10分)。
            2. 利多還是利空美元(DXY)？利多還是利空黃金(XAU)？
            3. 直接告訴我：符合我的SOP方向嗎？今晚開倉要多注意什麼？
            內容：{raw_news}
            """
            res = get_ai_response(prompt, api_key)
            if res: st.info(res)

    st.divider()

    # C. 劇本預演 (Scenario Planning)
    st.subheader("🎭 重磅數據劇本推演")
    c1, c2 = st.columns(2)
    with c1: event = st.text_input("待公布數據名稱", "例如：CPI")
    with c2: forecast = st.text_input("市場預期值", "例如：3.1%")
    
    if st.button("📝 生成三種交易劇本"):
        with st.spinner("推演中..."):
            prompt = f"數據{event}即將公布，預期{forecast}。請給出超預期、符合、低於預期三種情況下的黃金走勢推演，並特別針對 Funding Pips 5k 賬戶給出防禦性操作建議。"
            res = get_ai_response(prompt, api_key)
            if res: st.write(res)

# --- 模塊二：🔬 週末研究（策略進化、數據審計） ---
else:
    st.title("🔬 策略量化研究與進化")
    st.write("上傳包含 ATR、DXY狀態、MAEx、Fibo位置等維度的 CSV，找出 SOP 之外的死穴。")
    
    # A. 數據上傳
    uploaded_file = st.file_uploader("導入交易歷史 CSV", type="csv")
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.subheader("📊 數據樣本")
        st.dataframe(df.head(10))

        # B. 模式識別分析
        st.subheader("🧪 執行深度模式識別")
        additional_notes = st.text_area("補充你的主觀感悟 (例如：這兩周心態比較急)：")
        
        if st.button("🧪 開始量化分析共性"):
            with st.spinner("正在尋找隱藏變量..."):
                data_summary = df.to_string()
                prompt = f"""
                你是一名量化研究員。請審核以下數據。
                【我的 SOP】：{my_strategy}
                【交易數據】：{data_summary}
                【主觀背景】：{additional_notes}
                
                任務：
                1. 找出虧損單中除了 SOP 之外的【隱藏共同點】（時間、ATR、美元狀態等）。
                2. 分析 MAEx（最大反轉點數），告訴我現在 15pips 的止損緩衝是否合理？
                3. 評價 0.5R 減半止損機制是否真的優化了 Funding Pips 賬戶的生存率？
                4. 給出 2 條具體的進化建議。
                """
                res = get_ai_response(prompt, api_key)
                if res:
                    st.success("🔬 研究報告：")
                    st.markdown(res)

# --- 底部全局頁腳 ---
st.divider()
st.caption("TRADE AI | 專為職業交易員設計的進化終端 | $0 成本，無限可能")
