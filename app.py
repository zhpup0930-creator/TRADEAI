import streamlit as st
import google.generativeai as genai
import pandas as pd

# 网页设置：变成宽屏模式，更像交易终端
st.set_page_config(page_title="TRADE AI - 交易情报站", layout="wide")

# 自定义一些漂亮的样式
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border-radius: 10px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 侧边栏：配置中心 ---
with st.sidebar:
    st.title("⚙️ 配置中心")
    api_key = st.text_input("输入 Gemini API Key:", type="password")
    st.divider()
    st.info("建议品种：XAU/USD, EUR/USD, GBP/USD")
    mode = st.radio("系统模式：", ["基本面分析", "周末复盘(开发中)"])

# --- 主页面 ---
st.title("🛰️ 交易副驾：全天候情报过滤中心")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # 自动探测模型
        available_models = [m.name.replace('models/', '') for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model = genai.GenerativeModel(available_models[0])

        # --- 模块一：手动情报深度分析 ---
        st.subheader("📝 深度情报解剖")
        raw_news = st.text_area("粘贴金十快讯或任何宏观消息：", height=150, placeholder="例如：美联储官员鲍威尔表示...")
        
        if st.button("开始分析"):
            if raw_news:
                with st.spinner("AI 正在解剖宏观逻辑..."):
                    prompt = f"""
                    你是一个外汇/黄金高级分析师。分析这段文字：
                    1. 给出影响评分 (1-10分，10分为最强震荡)。
                    2. 标明对美元、黄金、欧元的具体方向影响。
                    3. 给出3个字以内的操作定调（如：看多、观望、做空）。
                    4. 最后用一段大白话总结。
                    内容：{raw_news}
                    """
                    response = model.generate_content(prompt)
                    st.info(response.text)
            else:
                st.warning("请输入内容")

        st.divider()

        # --- 模块二：剧本模拟（这就是我送你的额外赠品！） ---
        st.subheader("🎭 重磅数据“剧本推演”")
        col1, col2 = st.columns(2)
        with col1:
            event_name = st.text_input("输入数据名称", placeholder="例如：今晚非农")
            forecast_val = st.text_input("市场预期值", placeholder="例如：增加20万")
        with col2:
            current_bias = st.selectbox("当前黄金趋势", ["上涨趋势", "下跌趋势", "横盘震荡"])

        if st.button("生成交易剧本"):
            with st.spinner("正在推演各种可能..."):
                prompt = f"""
                即将公布 {event_name}，预期是 {forecast_val}。当前黄金是 {current_bias}。
                请帮我写出三种剧本：
                1. 如果公布值远超预期，黄金会怎么走？怎么操作？
                2. 如果公布值符合预期，黄金会怎么走？
                3. 如果公布值远低于预期，黄金会怎么走？怎么操作？
                用表格或条列式输出。
                """
                script = model.generate_content(prompt)
                st.write(script.text)

    except Exception as e:
        st.error(f"连接失败：{e}")
else:
    st.write("👈 请在左侧输入 API Key 启动大脑。")
    st.image("https://images.unsplash.com/photo-1611974714024-4607a507e605?auto=format&fit=crop&q=80&w=1000", caption="交易是孤独的修行，AI 是你的伴侣。")
