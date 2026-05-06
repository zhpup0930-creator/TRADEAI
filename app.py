import streamlit as st
import google.generativeai as genai
import pandas as pd
from PIL import Image # 处理图片的工具

# 网页设置
st.set_page_config(page_title="TRADE AI - 视觉副驾", layout="wide")

# --- 侧边栏：配置中心 ---
with st.sidebar:
    st.title("⚙️ 配置中心")
    api_key = st.text_input("输入 Gemini API Key:", type="password")
    st.divider()
    mode = st.radio("切换系统模式：", ["🛰️ 基本面分析 & 剧本", "📉 视觉毒舌复盘"])
    st.divider()
    st.info("💡 提示：复盘模式现在支持上传K线截图了！")

# --- AI 初始化函数 ---
def get_ai_response(prompt, key, image=None):
    genai.configure(api_key=key)
    # 自动获取可用模型 (Gemini 1.5 系列识图能力最强)
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # 优先找 1.5 系列，如果找不到就用第一个
    target_model = "gemini-1.5-flash" if "models/gemini-1.5-flash" in models else models[0].replace('models/', '')
    model = genai.GenerativeModel(target_model)
    
    if image:
        return model.generate_content([prompt, image]).text
    else:
        return model.generate_content(prompt).text

# --- 模式一：基本面分析 ---
if mode == "🛰️ 基本面分析 & 剧本":
    st.title("🛰️ 基本面情报 & 剧本推演")
    if api_key:
        with st.expander("📝 手动情报分析", expanded=True):
            raw_news = st.text_area("粘贴消息：")
            if st.button("分析"):
                st.info(get_ai_response(f"分析这段文字对黄金外汇影响：{raw_news}", api_key))
        
        st.subheader("🎭 数据剧本推演")
        c1, c2 = st.columns(2)
        with c1: event = st.text_input("数据名称")
        with c2: bias = st.selectbox("当前大趋势", ["上涨", "下跌", "震荡"])
        if st.button("生成推演"):
            st.write(get_ai_response(f"即将公布{event}，当前趋势{bias}，请给出三种走势剧本。", api_key))
    else:
        st.warning("👈 请先输入 API Key")

# --- 模式二：视觉毒舌复盘 (新增图片功能) ---
else:
    st.title("📉 视觉毒舌复盘教练")
    st.write("把你的【交易记录】和【当时做单的截图】传上来，让我看看你到底在干什么。")
    
    if api_key:
        col_up1, col_up2 = st.columns(2)
        with col_up1:
            csv_file = st.file_uploader("1. 上传交易记录 (CSV)", type="csv")
        with col_up2:
            img_file = st.file_uploader("2. 上传做单K线截图 (Optional)", type=["png", "jpg", "jpeg"])
        
        if img_file:
            st.image(img_file, caption="📸 已加载做单截图", width=500)

        if st.button("🔥 开始毒舌诊断"):
            with st.spinner("教练正在盯着屏幕分析你的神操..."):
                # 准备数据
                trade_data = pd.read_csv(csv_file).to_string() if csv_file else "未提供具体表格数据"
                
                # 组合 Prompt
                prompt = f"""
                你是一个外汇黄金圈最顶尖、最毒舌的职业教练。
                现在我有两份证据给你看：
                1. 我的文字记录数据：{trade_data}
                2. (如果你能看到图片) 这是我做单时的图表。
                
                请结合【图片里的技术面】和【文字里的开仓理由】：
                - 狠狠地羞辱我！找出图片里明显的错误（比如在压力位做多、无视超买信号等）。
                - 告诉我哪些细节我漏掉了，但图片里其实很明显。
                - 给我下周的必死禁令。
                不要废话，开始你的表演。
                """
                
                if img_file:
                    image = Image.open(img_file)
                    analysis = get_ai_response(prompt, api_key, image)
                else:
                    analysis = get_ai_response(prompt, api_key)
                
                st.error("🚨 教练最终诊断结果：")
                st.markdown(analysis)
    else:
        st.warning("👈 请先输入 API Key")
