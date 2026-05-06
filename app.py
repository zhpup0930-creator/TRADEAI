import streamlit as st
import google.generativeai as genai
import pandas as pd
import io

# 网页设置
st.set_page_config(page_title="TRADE AI - 终极副驾", layout="wide")

# --- 侧边栏：配置中心 ---
with st.sidebar:
    st.title("⚙️ 配置中心")
    api_key = st.text_input("输入 Gemini API Key:", type="password")
    st.divider()
    mode = st.radio("切换系统模式：", ["🛰️ 基本面分析 & 剧本", "📉 周末毒舌复盘"])
    st.divider()
    st.info("💡 提示：复盘模式请上传 CSV 格式的交易记录")

# --- AI 初始化 ---
def get_ai_response(prompt, key):
    genai.configure(api_key=key)
    # 自动获取可用模型
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    model = genai.GenerativeModel(models[0].replace('models/', ''))
    return model.generate_content(prompt).text

# --- 模式一：基本面分析 & 剧本 ---
if mode == "🛰️ 基本面分析 & 剧本":
    st.title("🛰️ 基本面情报 & 剧本推演")
    
    if api_key:
        # 手动分析模块
        with st.expander("📝 手动情报深度分析", expanded=True):
            raw_news = st.text_area("粘贴金十快讯或任何宏观消息：", height=100)
            if st.button("开始解剖消息"):
                res = get_ai_response(f"你是一个顶级分析师。分析这段文字对美元、黄金、欧元的影响，给出操作建议和大白话总结：{raw_news}", api_key)
                st.info(res)

        # 剧本推演模块
        st.subheader("🎭 重磅数据“剧本推演”")
        c1, c2, c3 = st.columns(3)
        with c1: event = st.text_input("数据名称", "非农就业数据")
        with c2: forecast = st.text_input("市场预期值", "20.5万")
        with c3: bias = st.selectbox("当前大趋势", ["上涨", "下跌", "震荡"])
        
        if st.button("生成交易剧本"):
            with st.spinner("推演中..."):
                prompt = f"即将公布{event}，预期{forecast}。当前趋势{bias}。请给出超预期、符合预期、低于预期三种情况下的黄金走势预测和操作建议。"
                st.write(get_ai_response(prompt, api_key))
    else:
        st.warning("👈 请先在左侧输入 API Key")

# --- 模式二：周末毒舌复盘 ---
else:
    st.title("📉 周末毒舌复盘教练")
    st.write("把你的交易记录(CSV)丢给我，让我看看你这周又犯了什么蠢。")
    
    if api_key:
        uploaded_file = st.file_uploader("上传交易记录 (CSV文件)", type="csv")
        
        if uploaded_file is not None:
            # 读取数据
            df = pd.read_csv(uploaded_file)
            st.write("📊 识别到的交易数据：", df.head(5)) # 显示前五行预览
            
            if st.button("开始毒舌分析"):
                with st.spinner("教练正在翻看你的烂账..."):
                    data_str = df.to_string()
                    prompt = f"""
                    你现在是一个极度严厉、毒舌的职业交易教练。
                    我会给你我这周的交易数据：{data_str}
                    请根据这些数据：
                    1. 算出我的胜率。
                    2. 找出我最大的亏损原因（是扛单？还是频繁交易？还是报复性开仓？）。
                    3. 像黑脸教练一样骂我，指出我最愚蠢的操作，并给我下周的3条硬性纪律。
                    不要客气，越直接越好。
                    """
                    analysis = get_ai_response(prompt, api_key)
                    st.error("🚨 教练评语：")
                    st.write(analysis)
    else:
        st.warning("👈 请先在左侧输入 API Key")
