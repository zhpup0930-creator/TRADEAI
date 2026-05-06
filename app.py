import streamlit as st
import google.generativeai as genai
import pandas as pd

# 网页设置
st.set_page_config(page_title="TRADE AI - 策略进化分析终端", layout="wide")

# --- 侧边栏：核心配置 ---
with st.sidebar:
    st.title("🔬 策略量化研究室")
    api_key = st.text_input("1. 输入 Gemini API Key:", type="password")
    
    st.divider()
    st.subheader("📜 我的 SOP 定义")
    my_strategy = st.text_area(
        "输入你目前执行的 SOP 规则：", 
        height=250,
        placeholder="AI将以此为基准，分析数据中的违规或偏差..."
    )
    
    st.divider()
    st.info("💡 建议：上传包含时间、品种、盈亏、DXY状态、RSI数值、交易时段等多维度的 CSV 文件。数据越细，发现越深。")

# --- AI 初始化 ---
def get_ai_response(prompt, key):
    genai.configure(api_key=key)
    # 获取可用模型
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = "gemini-1.5-flash" if "models/gemini-1.5-flash" in models else models[0].replace('models/', '')
    model = genai.GenerativeModel(target_model)
    return model.generate_content(prompt).text

# --- 主界面 ---
st.title("📈 交易数据深度模式识别 (Pattern Recognition)")
st.write("不看图片，只看数据。让 AI 找出你盈利与亏损背后的【隐藏变量相关性】。")

if api_key:
    # 1. 上传 CSV
    uploaded_file = st.file_uploader("导入历史交易流水 (CSV)", type="csv")
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.subheader("📊 待审计数据预览")
        st.dataframe(df) # 显示完整表格

        # 2. 补充场景描述
        st.subheader("📝 补充上下文")
        additional_context = st.text_area("对于这段时间的市场环境或你的状态，有什么需要补充的？", height=80)

        # 3. 深度分析按钮
        if st.button("🧪 执行隐藏变量分析"):
            if not my_strategy:
                st.error("请先在左侧定义 SOP，否则 AI 无法对比差异！")
            else:
                with st.spinner("正在进行多维度聚类分析，寻找盈亏潜在规律..."):
                    data_str = df.to_string()
                    
                    prompt = f"""
                    你是一名资深的量化交易研究员和数据科学家。请根据以下数据进行【关联性分析】。
                    
                    【我的 SOP 规则】：
                    "{my_strategy}"
                    
                    【详细交易数据】：
                    "{data_str}"
                    
                    【背景补充】：
                    "{additional_context}"
                    
                    你的任务：
                    1. 【盈亏共性挖掘】：
                       - 找出亏损单中，除了违反SOP之外的共同“隐藏变量”（例如：是否集中在某个时间段？是否当时的DXY都在某种特定状态？是否RSI在特定区间？）。
                       - 找出盈利单中，除了符合SOP之外的共同“加分项”。
                    2. 【SOP 压力测试】：
                       - 现有的 SOP 在什么样的情况下表现最差？（比如：低波动率环境？纽约盘开盘时？）
                    3. 【数据相关性报告】：
                       - 分析“信心值”与“实际盈亏”的相关性。
                       - 分析“交易时段(Session)”对胜率的影响。
                    4. 【进化建议】：
                       - 给出 2-3 条定量的 SOP 修改建议。例如：“当 DXY 处于 XXX 状态时，即便符合 SOP 也不入场。”
                    
                    请保持绝对理性，完全基于数据事实，给出深度分析报告。
                    """
                    
                    analysis = get_ai_response(prompt, api_key)
                    st.success("🔬 策略进化研究报告已生成：")
                    st.markdown(analysis)
else:
    st.warning("👈 请输入 API Key 启动系统")
