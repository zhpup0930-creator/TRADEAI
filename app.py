import streamlit as st
import google.generativeai as genai

# 网页的标题和设置
st.set_page_config(page_title="我的交易大脑", layout="centered")
st.title("💡 专属外汇/黄金交易军师")

# 1. 钥匙插孔（安全起见，钥匙不写死在代码里，由你在这个网页上输入）
api_key = st.text_input("🔑 请输入你的 Gemini API Key 解锁系统：", type="password")

if api_key:
    try:
        # 2. 激活 AI 大脑
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        st.success("✅ AI 大脑已连接！")
        
        # 3. 第一个功能测试：大白话翻译机
        st.subheader("📰 基本面大白话翻译机")
        news_input = st.text_area("请把金十数据或者你不懂的新闻粘贴在这里：")
        
        if st.button("开始分析新闻"):
            with st.spinner("军师正在极速分析中..."):
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
        st.error(f"连接失败，请检查 API Key 是否正确。错误信息：{e}")
else:
    st.warning("👈 请先在上方输入你的 API Key 以启动系统。")
