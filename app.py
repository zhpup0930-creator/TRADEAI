import streamlit as st
import google.generativeai as genai
import pandas as pd
import feedparser

# 1. 网页设置
st.set_page_config(page_title="TRADE AI - 5星预警终端", layout="wide")

# --- 侧边栏：核心配置 ---
with st.sidebar:
    st.title("🛡️ 5星预警终端")
    api_key = st.text_input("🔑 输入 API Key:", type="password")
    
    st.divider()
    menu = st.radio(
        "工作模式：",
        ["💣 5星级核弹快讯", "🔬 策略量化研究室"]
    )
    
    st.divider()
    st.subheader("📜 核心 SOP")
    default_sop = "【環境】：H1 ATR > 5 | 【結構】：H1 同色K線 -> Fibo | 【進場】：M5 0.618 + 吞沒 | 【防禦】：0.5R止損減半"
    my_strategy = st.text_area("当前 SOP 规则：", value=default_sop, height=150)

# --- AI 核心函数 (自动匹配模型) ---
def get_ai_response(prompt, key):
    if not key: return None
    try:
        genai.configure(api_key=key)
        available_models = [m.name.replace('models/', '') for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        best_model = "gemini-1.5-flash" if "gemini-1.5-flash" in available_models else available_models[0]
        model = genai.GenerativeModel(best_model)
        return model.generate_content(prompt).text
    except Exception as e:
        return f"AI 异常: {e}"

# --- 功能：抓取全球新闻流 ---
def fetch_raw_data():
    rss_url = "https://search.cnbc.com/rs/search/view.xml?partnerId=2000&keywords=macroeconomics&sort=date"
    feed = feedparser.parse(rss_url)
    return "\n\n".join([f"标题: {e.title} \n摘要: {e.summary}" for e in feed.entries[:15]])

# --- 模块一：💣 5星级核弹快讯 ---
if menu == "💣 5星级核弹快讯":
    st.title("💣 5星级宏观核弹预警")
    st.write("系统会自动过滤所有低价值噪音，只有达到 5 星级（影响评分 >= 9）的资讯才会显示。")
    
    if st.button("🚀 扫描昨夜至今的 5 星事件"):
        with st.spinner("正在排查垃圾信息..."):
            raw_data = fetch_raw_data()
            prompt = f"""
            你是一名极其严苛的黄金/外汇首席风控官。
            请分析以下新闻流：
            {raw_data}
            
            任务：
            1. 严格过滤：只有能让 XAUUSD 或美元指数产生重磅波动（打分必须 >= 9）的事件才准许输出。
            2. 如果没有任何 5 星级大事，请只回答：“当前市场暂无 5 星级核弹新闻。”
            3. 如果有，请用大红色的警告语气列出事件。
            4. 结合我的 SOP ({my_strategy}) 给出最直接的防守指令。
            """
            result = get_ai_response(prompt, api_key)
            if "暂无" in result:
                st.info(result)
            else:
                st.error("🚨 探测到 5 星级影响事件！")
                st.markdown(result)

    st.divider()
    st.subheader("📝 手动快讯查验")
    user_news = st.text_area("粘贴你想确认的一条快讯：", placeholder="AI 将判断这是否值得你关注...")
    if st.button("查验级别") and api_key:
        check_prompt = f"分析此消息影响力。如果评分不足 9 分，请直接告诉交易员‘这是噪音，不用理会’。如果超过 9 分，请分析对黄金的具体冲击。消息：{user_news}"
        st.warning(get_ai_response(check_prompt, api_key))

# --- 模块二：🔬 策略量化研究室 ---
else:
    st.title("🔬 策略量化与模式识别")
    st.write("上传你的 CSV 交易记录，AI 将找出人类肉眼看不见的【盈利/亏损隐藏共性】。")
    
    uploaded_file = st.file_uploader("导入 CSV 历史数据", type="csv")
    if uploaded_file and api_key:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head(5))
        
        if st.button("🧪 开启深度量化审计"):
            with st.spinner("正在进行多维度聚类分析..."):
                data_str = df.to_string()
                prompt = f"""
                你是一名量化数据科学家。
                【SOP】：{my_strategy}
                【数据】：{data_str}
                任务：
                1. 找出亏损单中除了 SOP 之外的【隐藏共性】（时间、ATR、美元状态、RSI等）。
                2. 告诉交易员他在哪种特定环境下必亏。
                3. 给出现有 SOP 的进化建议。
                """
                st.markdown(get_ai_response(prompt, api_key))

# 底部
st.divider()
st.caption("TRADE AI | 极致过滤 | 深度进化")
