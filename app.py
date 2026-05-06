import streamlit as st
import google.generativeai as genai
import pandas as pd
from PIL import Image
import io

# 网页设置
st.set_page_config(page_title="TRADE AI - 策略进化实验室", layout="wide")

# --- 侧边栏：核心配置 ---
with st.sidebar:
    st.title("🧪 策略进化实验室")
    api_key = st.text_input("1. 输入 Gemini API Key:", type="password")
    
    st.divider()
    st.subheader("📜 当前 SOP 定义")
    my_strategy = st.text_area(
        "输入你目前执行的 SOP 规则：", 
        height=200,
        placeholder="AI将以此为基准，寻找超出规则之外的隐藏变量..."
    )
    
    st.divider()
    mode = st.radio("系统功能：", ["🛰️ 宏观情报推演", "🔍 多单关联模式识别"])
    st.info("💡 核心逻辑：通过分析多笔交易的成败，找出人类肉眼无法察觉的‘隐藏变量’，进化你的 SOP。")

# --- AI 初始化 ---
def get_ai_response(prompt, key, images=None):
    genai.configure(api_key=key)
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = "gemini-1.5-flash" if "models/gemini-1.5-flash" in models else models[0].replace('models/', '')
    model = genai.GenerativeModel(target_model)
    
    content_list = [prompt]
    if images:
        content_list.extend(images)
    return model.generate_content(content_list).text

# --- 功能一：宏观推演 (保留) ---
if mode == "🛰️ 宏观情报推演":
    st.title("🛰️ 宏观推演 & 情景规划")
    raw_news = st.text_area("粘贴近期核心资讯：")
    if st.button("生成理性解构"):
        st.info(get_ai_response(f"作为理性分析师，解构此消息对XAU/USD的影响概率：{raw_news}", api_key))

# --- 功能二：多单关联模式识别 (深度进化) ---
else:
    st.title("🔍 隐藏模式识别与策略进化")
    st.write("上传多笔交易记录，让 AI 找出连你自己都还没察觉到的【盈亏隐藏共性】。")
    
    if api_key:
        # 上传区
        uploaded_file = st.file_uploader("导入多笔历史交易 CSV (需包含盈亏、时间、理由等)", type="csv")
        
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.write("📊 待分析的数据样本：", df)
            
            st.divider()
            st.subheader("📝 补充细节（可选）")
            additional_context = st.text_area("针对这些单子，有没有什么你想补充的盘感或细节？", height=100)

            if st.button("🧪 执行大数据模式识别"):
                with st.spinner("AI 正在深度扫描数据间的底层逻辑关联..."):
                    # 数据字符串化
                    data_summary = df.to_string()
                    
                    # 深度科研级 Prompt
                    prompt = f"""
                    你现在是一名顶级的量化交易研究员，专门负责从资深交易员的成交数据中发现“肉眼不可见的偏差”。
                    
                    【交易员现有的 SOP】：
                    "{my_strategy}"
                    
                    【多笔历史交易数据】：
                    "{data_summary}"
                    
                    【额外背景信息】：
                    "{additional_context}"
                    
                    你的任务是进行“聚类关联分析”，不要评价单子对错，只需找出以下隐藏模式：
                    1. 【亏损单的隐藏共性】：在所有亏损单中，除了符合SOP外，是否存在共同的“环境因素”？(例如：是否都在特定的时间段？是否都在DXY某种走势下？是否开仓前的K线形态有某种微小的一致性？)
                    2. 【盈利单的隐形成色】：在那些大盈单中，有没有哪个技术指标或盘面细节是SOP里没写、但它们都共同具备的？
                    3. 【SOP 进化建议】：基于以上发现，请给出具体的、定量的建议，如何微调现有的SOP以过滤掉那些“看起来完美但大概率失败”的陷阱？
                    4. 【变量相关性测试】：如果数据中有时间数据，分析交易质量与时间窗口（如伦敦/纽约盘交替）的相关性。
                    
                    请用极其理性、数据驱动、证据导向的方式输出报告。
                    """
                    
                    analysis = get_ai_response(prompt, api_key)
                    st.success("🔬 策略进化研究报告：")
                    st.markdown(analysis)
    else:
        st.warning("👈 请输入 API Key")
