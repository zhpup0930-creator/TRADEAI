import streamlit as st
import google.generativeai as genai
import pandas as pd
from PIL import Image

# 网页设置：保持极简专业风
st.set_page_config(page_title="TRADE AI - 理性分析终端", layout="wide")

# --- 侧边栏：配置中心 ---
with st.sidebar:
    st.title("⚖️ 逻辑风控中心")
    api_key = st.text_input("输入 Gemini API Key:", type="password")
    st.divider()
    mode = st.radio("系统模式：", ["🛰️ 宏观基本面推演", "🧬 交易逻辑科学复盘"])
    st.divider()
    st.info("💡 理念：排除情绪干扰，尊重客观事实与概率理论。")

# --- AI 初始化函数 ---
def get_ai_response(prompt, key, images=None):
    genai.configure(api_key=key)
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = "gemini-1.5-flash" if "models/gemini-1.5-flash" in models else models[0].replace('models/', '')
    model = genai.GenerativeModel(target_model)
    
    content_list = [prompt]
    if images:
        content_list.extend(images)
        
    return model.generate_content(content_list).text

# --- 模式一：宏观基本面推演 ---
if mode == "🛰️ 宏观基本面推演":
    st.title("🛰️ 宏观经济数据分析 & 预期推演")
    if api_key:
        with st.expander("📝 市场资讯客观分析", expanded=True):
            raw_news = st.text_area("请粘贴快讯或政策声明：", placeholder="AI将基于宏观逻辑进行理性解析...")
            if st.button("开始逻辑解构"):
                prompt = f"""
                请以职业宏观交易员的身份，对以下内容进行绝对理性的解构：
                1. 核心变量：提取对市场起决定性作用的经济参数。
                2. 传导路径：该资讯如何通过美元指数(DXY)传导至黄金(XAU)和外汇市场。
                3. 概率分布：基于历史经验，价格向上或向下波动的可能性评估。
                
                内容：{raw_news}
                """
                st.info(get_ai_response(prompt, api_key))
        
        st.subheader("🎭 关键数据情景模拟 (Scenario Planning)")
        c1, c2 = st.columns(2)
        with c1: event = st.text_input("待公布数据", "例如：非农(NFP)")
        with c2: bias = st.selectbox("当前技术面基调", ["看涨结构", "看跌结构", "区间震荡"])
        if st.button("执行情景推演"):
            prompt = f"分析{event}对市场预期的影响。结合当前{bias}，请给出：偏离预期、符合预期、低于预期的三种理性应对方案。"
            st.write(get_ai_response(prompt, api_key))
    else:
        st.warning("👈 请输入 API Key 启动系统")

# --- 模式二：科学复盘 (理性纠偏版) ---
else:
    st.title("🧬 交易逻辑科学复盘")
    st.write("本模块通过【证据比对】与【理论验证】，客观评估交易质量。")
    
    if api_key:
        # 第一步：多维证据收集
        c_up1, c_up2 = st.columns(2)
        with c_up1:
            csv_file = st.file_uploader("1. 导入交易历史 (CSV)", type="csv")
        with c_up2:
            img_files = st.file_uploader("2. 导入K线技术截图 (支持多周期比对)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
        
        if img_files:
            cols = st.columns(len(img_files))
            for i, f in enumerate(img_files):
                cols[i].image(f, caption=f"技术位证据 {i+1}", use_container_width=True)

        st.divider()

        # 第二步：开仓逻辑陈述
        st.subheader("📖 交易员逻辑陈述 (Context)")
        user_story = st.text_area(
            "请客观描述你的开仓逻辑：", 
            height=150, 
            placeholder="请陈述：你的入场信号、止损依据、预期盈亏比，以及你当时观察到的技术/基本面证据。"
        )

        # 第三步：科学分析按钮
        if st.button("⚖️ 执行逻辑一致性分析"):
            if not img_files and not user_story:
                st.warning("请至少提供逻辑描述或图表截图以供分析。")
            else:
                with st.spinner("正在检索技术理论并比对盘面证据..."):
                    # 数据处理
                    trade_data = pd.read_csv(csv_file).to_string() if csv_file else "无表格记录"
                    images_data = [Image.open(f) for f in img_files] if img_files else []
                    
                    # 绝对理性的 Prompt
                    prompt = f"""
                    你是一名资深的交易心理医生与风控专家，说话风格保持【绝对中立、理性、证据导向】。
                    
                    【交易员陈述】：
                    "{user_story}"
                    
                    【客观交易数据】：
                    "{trade_data}"
                    
                    任务：请对比上述自述与提供的K线图片（如果存在），进行多维度逻辑验证：
                    
                    1. 【逻辑与事实的一致性】：交易员自述的逻辑（如支撑位、信号）在图片中是否清晰可辨且成立？是否存在“幻觉交易”？
                    2. 【技术面盲区】：基于图片展示的多个周期，是否存在交易员未提及但极其关键的负面证据（如隐藏的阻力位、指标背离、时间窗口冲突）？
                    3. 【风险评估】：该笔交易的入场点与止损设计是否符合概率优势？盈亏比是否健康？
                    4. 【最终定性】：
                       - 属于“高质量亏损”（逻辑严密，符合系统，输给概率）；
                       - 还是“系统外亏损”（逻辑存在明显缺陷，属于低质量操作）。
                    5. 【优化建议】：基于理论和事实，下一次遇到同类情况，最佳的修正方案是什么？
                    
                    请给出基于证据的分析，严禁使用攻击性、情绪化语言。
                    """
                    
                    analysis = get_ai_response(prompt, api_key, images_data)
                    
                    st.success("📝 逻辑一致性分析报告：")
                    st.markdown(analysis)
    else:
        st.warning("👈 请输入 API Key")
