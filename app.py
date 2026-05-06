import streamlit as st
import google.generativeai as genai

# 网页的标题和设置
st.set_page_config(page_title="我的交易大脑", layout="centered")
st.title("💡 专属外汇/黄金交易军师")

# 1. 钥匙插孔
api_key = st.text_input("🔑 请输入你的 Gemini API Key 解锁系统：", type="password")

if api_key:
    try:
        # 2. 激活并自动侦测可用的大脑
        genai.configure(api_key=api_key)
        
        # 强行搜查可用的模型
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name.replace('models/', ''))
        
        if not available_models:
            st.error("❌ 你的 API Key 无法获取模型，可能是接口权限未开通。")
        else:
            # 自动选择列表里的第一个可用模型
            best_model_name = available_models[0]
            st.success(f"✅ AI 大脑已连接！系统已自动为你匹配最强节点：{best_model_name}")
            
            model = genai.GenerativeModel(best_model_name)
            
            # 3. 核心功能：大白话翻译机
            st.subheader("📰 基本面大白话翻译机")
            news_input = st.text_area("请把金十数据或者你不懂的新闻粘贴在这里：")
            
            if st.button("开始分析新闻"):
                with st.spinner("军师正在极速分析中，请稍候..."):
                    # 设定 AI 的角色和任务
                    prompt = f"""
                    你现在是一名顶级的华尔街宏观外汇交易员。
                    请分析以下新闻，并直接告诉我：
                    1. 这条新闻对美元指数(DXY)是利多还是利空？
                    2. 对黄金(XAU/USD)和欧元(EUR/USD)会有什么方向的影响？
                    3. 用大白话总结，说人话。
                    
                    新闻内容：{news_input}
                    """
                    response = model.generate_content(prompt)
                    st.write(response.text)
                    
    except Exception as e:
        st.error(f"连接失败，错误信息：{e}")
else:
    st.warning("👈 请先在上方输入你的 API Key 以启动系统。")
