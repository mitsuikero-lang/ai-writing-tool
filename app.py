import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AIライティングツール",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# サイドバー
with st.sidebar:
    st.title("AIライティングツール")
    st.markdown("---")

    # APIキー設定
    api_key_env = os.getenv("GEMINI_API_KEY", "")
    if not api_key_env:
        api_key_input = st.text_input(
            "Gemini APIキー",
            type="password",
            placeholder="AIzaSy...",
            help=".envファイルに GEMINI_API_KEY を設定するか、ここに直接入力してください。",
        )
        if api_key_input:
            os.environ["GEMINI_API_KEY"] = api_key_input
    else:
        st.success("APIキー設定済み")

    st.markdown("---")

    # ツール選択
    selected = st.radio(
        "ツール選択",
        [
            "ブログ記事執筆",
            "メール返信文作成",
            "文章要約",
            "文章校正・リライト",
            "SNS投稿文作成",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")

    # モデル選択
    model_name = st.selectbox(
        "モデル",
        [
            "gemini-2.5-flash-lite",
            "gemini-2.5-flash",
            "gemini-2.5-pro",
        ],
        help="gemini-2.5-flash-liteは高速でコスパ良好。gemini-2.5-proは最高精度。",
    )
    st.session_state["model_name"] = model_name

    st.caption("Powered by Gemini API")

# APIキー未設定の場合は案内を表示
if not os.getenv("GEMINI_API_KEY"):
    st.warning("サイドバーにGemini APIキーを入力してください。")
    st.markdown(
        "APIキーは [Google AI Studio](https://aistudio.google.com/apikey) から取得できます。"
    )
    st.stop()

# 各ツールを表示
if selected == "ブログ記事執筆":
    from tools.blog_writer import render_blog_writer
    render_blog_writer()

elif selected == "メール返信文作成":
    from tools.email_reply import render_email_reply
    render_email_reply()

elif selected == "文章要約":
    from tools.summarizer import render_summarizer
    render_summarizer()

elif selected == "文章校正・リライト":
    from tools.proofreader import render_proofreader
    render_proofreader()

elif selected == "SNS投稿文作成":
    from tools.sns_writer import render_sns_writer
    render_sns_writer()
