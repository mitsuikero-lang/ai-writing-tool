import streamlit as st
from utils.gemini_client import generate_text


def render_summarizer():
    st.header("文章要約")
    st.caption("長い文章を入力すると、指定した条件で要約します。")

    with st.form("summarizer_form"):
        text = st.text_area(
            "要約したい文章 *",
            placeholder="ここに要約したいテキストを貼り付けてください...",
            height=250,
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            length = st.selectbox(
                "要約の長さ",
                ["短め（100字程度）", "標準（200〜300字）", "詳しめ（400〜500字）"],
            )
        with col2:
            format_type = st.selectbox(
                "出力形式",
                ["文章形式", "箇条書き（3〜5点）", "箇条書き（詳細）", "文章＋箇条書き"],
            )
        with col3:
            focus = st.selectbox(
                "要約の視点",
                [
                    "全体的に均等",
                    "重要なポイントに集中",
                    "結論・結果に集中",
                    "数字・データに集中",
                ],
            )

        submitted = st.form_submit_button(
            "要約する", type="primary", use_container_width=True
        )

    if submitted:
        if not text:
            st.error("要約したい文章を入力してください。")
            return

        original_length = len(text)

        with st.spinner("要約中..."):
            prompt = _build_prompt(text, length, format_type, focus)
            try:
                result = generate_text(prompt, temperature=0.3)
                summary_length = len(result)
                compression = max(0, int((1 - summary_length / original_length) * 100))

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("元の文字数", f"{original_length:,}字")
                with col2:
                    st.metric("要約後の文字数", f"{summary_length:,}字")
                with col3:
                    st.metric("圧縮率", f"{compression}%")

                st.markdown("---")
                st.subheader("要約結果")
                st.markdown(result)

                st.download_button(
                    "要約をダウンロード",
                    result,
                    file_name="summary.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")


def _build_prompt(text, length, format_type, focus):
    return f"""以下の文章を要約してください。

【原文】
{text}

【要約の条件】
長さ: {length}
出力形式: {format_type}
要約の視点: {focus}

条件に従って正確に要約してください。重要な情報を漏らさず、簡潔にまとめてください。"""
