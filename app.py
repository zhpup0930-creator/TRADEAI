import streamlit as st
import google.generativeai as genai
import pandas as pd
from PIL import Image

# 网页设置
st.set_page_config(page_title="TRADE AI - 策略审计终端", layout="wide")

# --- 侧边栏：核心配置 ---
with st.sidebar:
    st.title("🛡️ 策略审计中心")
    api_key = st.text_input("1. 输入 Gemini API Key:", type="password")
    
    st.divider()
    # 新增：策略定义区
    st.subheader("📜 我的交易系统定义")
    my_strategy = st.text_area(
        "在此输入你的核心策略规则（AI将以此为唯一准则）：", 
        height=300,
        placeholder="例如：\n1. 只做H4级别趋势方向。\n2. 入场条件：M15出现底分型+RSI超卖。\n3. 止损：前高/前低外2点。\n4. 盈亏比低于1:2不接单。"
    )
    
    st.divider()
    mode = st.radio("系统模式：", ["🛰️ 宏观情报推演", "⚖️ 策略合规性复盘"])
    st.info("提示：AI 现在会根据上面定义的规则来审计你的每一笔交易。")

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

# --- 模式一：宏观基本面 ---
if mode == "🛰️ 宏观情报推演":
    st.title("🛰️ 宏观经济逻辑推演")
    if api_key:
        raw_news = st.text_area("粘贴市场资讯：")
        if st.button("开始理性解构"):
            prompt = f"请以职业分析师身份，基于宏观逻辑分析以下内容对美元、黄金、外汇的概率影响：{raw_news}"
            st.info(get_ai_response(prompt, api_key))
    else:
        st.warning("👈 请先输入 API Key")

# --- 模式二：策略合规性复盘 (核心升级) ---
else:
    st.title("⚖️ 策略合规性审计复盘")
    st.write("本模块不再进行通用评价，而是严格审计你的操作是否符合【你的个人策略】。")
    
    if api_key:
        # 第一步：证据收集
        c1, c2 = st.columns(2)
        with c1:
            csv_file = st.file_uploader("导入记录 (CSV)", type="csv")
        with c2:
            img_files = st.file_uploader("导入K线证据 (多张)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
        
        if img_files:
            cols = st.columns(len(img_files))
            for i, f in enumerate(img_files):
                cols[i].image(f, use_container_width=True)

        st.divider()

        # 第二步：单笔交易描述
        st.subheader("📖 当前单子逻辑自述")
        user_story = st.text_area("请描述这一单的入场细节：", height=100, placeholder="描述你当时觉得符合了哪几条策略规则...")

        # 第三步：执行分析
        if st.button("⚖️ 执行策略一致性审计"):
            if not my_strategy:
                st.error("🚨 请先在左侧【侧边栏】定义你的交易策略规则！否则AI无法进行审计。")
            elif not img_files and not user_story:
                st.warning("请提供描述或图片。")
            else:
                with st.spinner("正在根据你的策略标准，对比盘面证据进行审计..."):
                    # 数据准备
                    images_data = [Image.open(f) for f in img_files] if img_files else []
                    
                    # 极其严谨的审计 Prompt
                    prompt = f"""
                    你是一名专业的【交易合规审计官】。你的唯一任务是：判断交易员的操作是否严格遵守了他自己定义的策略。
                    
                    【交易员定义的策略规则】：
                    "{my_strategy}"
                    
                    【交易员对该笔单子的自述】：
                    "{user_story}"
                    
                    任务指令：
                    1. 【合规性审计】：逐条对照策略规则。该单子在【图片证据】中是否真实体现了规则要求的信号？
                    2. 【违规项识别】：如果交易员违背了自己的规则（例如：规则要求H4顺势，但图片显示他在逆势），请清晰、理性地指出，并引用图片细节。
                    3. 【执行质量评价】：如果规则都遵守了，但还是亏损了，请分析这是否属于“合理的概率成本”？还是进场点位可以更优化？
                    4. 【最终审计结论】：
                       - [✅ 合规交易]：逻辑完美闭环，亏损属于概率。
                       - [⚠️ 违规交易]：未遵守自身定义的策略。
                    5. 【修正建议】：为了确保下一次操作合规，他需要注意哪个具体的观察点？
                    
                    请保持绝对理性，以证据为准，严禁使用情绪化语言。
                    """
                    
                    analysis = get_ai_response(prompt, api_key, images_data)
                    st.success("📝 策略合规性审计报告：")
                    st.markdown(analysis)
    else:
        st.warning("👈 请输入 API Key")
