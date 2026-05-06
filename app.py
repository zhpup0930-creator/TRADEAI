import streamlit as st
import google.generativeai as genai
import pandas as pd
from PIL import Image

# 网页设置
st.set_page_config(page_title="TRADE AI - 多维副驾", layout="wide")

# --- 侧边栏：配置中心 ---
with st.sidebar:
    st.title("⚙️ 配置中心")
    api_key = st.text_input("输入 Gemini API Key:", type="password")
    st.divider()
    mode = st.radio("切换系统模式：", ["🛰️ 基本面分析 & 剧本", "📉 多图毒舌复盘"])
    st.divider()
    st.info("💡 建议：复盘时上传不同周期的截图（如M15+H1+H4）")

# --- AI 初始化函数 ---
def get_ai_response(prompt, key, images=None):
    genai.configure(api_key=key)
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # 识图必须用支持多模态的模型，这里强制尝试使用 flash 版本，速度快且支持多图
    target_model = "gemini-1.5-flash" if "models/gemini-1.5-flash" in models else models[0].replace('models/', '')
    model = genai.GenerativeModel(target_model)
    
    # 构造输入列表：先放文字 Prompt，后面跟着所有的图片内容
    content_list = [prompt]
    if images:
        content_list.extend(images)
        
    return model.generate_content(content_list).text

# --- 模式一：基本面分析 ---
if mode == "🛰️ 基本面分析 & 剧本":
    st.title("🛰️ 基本面情报 & 剧本推演")
    if api_key:
        with st.expander("📝 手动情报分析", expanded=True):
            raw_news = st.text_area("粘贴金十消息：")
            if st.button("开始解剖"):
                st.info(get_ai_response(f"分析这段文字对黄金外汇影响：{raw_news}", api_key))
        
        st.subheader("🎭 数据剧本推演")
        c1, c2 = st.columns(2)
        with c1: event = st.text_input("数据名称", "例如：CPI")
        with c2: bias = st.selectbox("当前大趋势", ["上涨", "下跌", "震荡"])
        if st.button("生成推演剧本"):
            st.write(get_ai_response(f"即将公布{event}，当前趋势{bias}，请给出三种走势剧本。", api_key))
    else:
        st.warning("👈 请先输入 API Key")

# --- 模式二：多图毒舌复盘 (升级版) ---
else:
    st.title("📉 多图毒舌复盘教练")
    st.write("上传你的交易记录和【多张】K线截图（入场点、不同周期图、指标图）。")
    
    if api_key:
        csv_file = st.file_uploader("1. 上传交易记录 (CSV)", type="csv")
        # 修改这里：accept_multiple_files=True 允许选多张图
        img_files = st.file_uploader("2. 上传多张K线截图 (最多5张)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
        
        if img_files:
            cols = st.columns(len(img_files))
            for i, f in enumerate(img_files):
                cols[i].image(f, caption=f"图片 {i+1}", use_container_width=True)

        if st.button("🔥 开始全维度毒舌诊断"):
            if not csv_file and not img_files:
                st.warning("请至少提供数据或图片！")
            else:
                with st.spinner("教练正在对比多个周期的图表，寻找你的作死证据..."):
                    # 处理 CSV 数据
                    trade_data = pd.read_csv(csv_file).to_string() if csv_file else "未提供具体表格数据"
                    
                    # 处理图片数据
                    images_data = []
                    if img_files:
                        for f in img_files:
                            images_data.append(Image.open(f))
                    
                    # 组合增强版 Prompt
                    prompt = f"""
                    你是一个外汇黄金圈最顶尖、最刻薄、眼睛最毒的职业教练。
                    我会给你提供：
                    1. 我的文字记录：{trade_data}
                    2. 我上传的几张关联截图（可能是不同周期的K线，或者入场出场的对比图）。
                    
                    请你【综合看这几张图】：
                    - 重点检查多周期一致性：比如是不是在小周期看多，但大周期明明是强压力位？
                    - 拆穿我的谎言：我的理由和图片里的实际情况对得上吗？
                    - 找出我漏掉的技术细节。
                    - 用最狠的话骂醒我，并给我下周的硬性规矩。
                    """
                    
                    analysis = get_ai_response(prompt, api_key, images_data)
                    
                    st.error("🚨 深度诊断报告：")
                    st.markdown(analysis)
    else:
        st.warning("👈 请先输入 API Key")
