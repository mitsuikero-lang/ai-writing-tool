import streamlit as st
from utils.gemini_client import generate_text


def render_blog_writer():
    st.header("ブログ記事執筆")
    st.caption("テーマや条件を入力すると、ブログ記事を自動生成します。")

    with st.form("blog_form"):
        topic = st.text_input(
            "記事のテーマ・タイトル *",
            placeholder="例：初心者向けPythonプログラミング入門",
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            target = st.selectbox(
                "ターゲット読者",
                ["一般読者", "初心者向け", "中級者向け", "専門家向け"],
            )
        with col2:
            word_count = st.selectbox(
                "文字数目安",
                ["500〜800字", "800〜1200字", "1200〜2000字", "2000字以上"],
            )
        with col3:
            style = st.selectbox(
                "文体",
                ["です・ます体", "だ・である体", "カジュアル"],
            )

        keywords = st.text_input(
            "SEOキーワード（任意・カンマ区切り）",
            placeholder="例：Python, プログラミング, 入門",
        )
        additional = st.text_area(
            "追加の指示（任意）",
            placeholder="例：見出しを5つ含めてください。具体的なコード例も入れてください。",
            height=80,
        )

        submitted = st.form_submit_button(
            "記事を生成", type="primary", use_container_width=True
        )

    if submitted:
        if not topic:
            st.error("記事のテーマを入力してください。")
            return

        with st.spinner("記事を生成中..."):
            prompt = _build_prompt(topic, target, word_count, style, keywords, additional)
            try:
                result = generate_text(prompt, temperature=0.8)
                st.success("生成完了！")
                st.markdown("---")

                with st.expander("生成された記事", expanded=True):
                    st.markdown(result)

                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "Markdownでダウンロード",
                        result,
                        file_name=f"{topic[:20]}.md",
                        mime="text/markdown",
                        use_container_width=True,
                    )
                with col2:
                    st.download_button(
                        "テキストでダウンロード",
                        result,
                        file_name=f"{topic[:20]}.txt",
                        mime="text/plain",
                        use_container_width=True,
                    )
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")


def _build_prompt(topic, target, word_count, style, keywords, additional):
    parts = [
        "以下の条件でブログ記事を執筆してください。",
        "",
        f"テーマ: {topic}",
        f"ターゲット読者: {target}",
        f"文字数: {word_count}",
        f"文体: {style}",
    ]
    if keywords:
        parts.append(f"SEOキーワード（本文中に自然に含めること）: {keywords}")
    if additional:
        parts.append(f"追加の指示: {additional}")

    parts += [
        "",
        "以下の構成で書いてください：",
        "1. 魅力的な導入文（読者の興味を引く）",
        "2. 本文（H2見出しを使って整理し、各セクションに具体的な内容を書く）",
        "3. まとめ（読者へのアクション促進）",
        "",
        "マークダウン形式で出力してください。",
    ]
    return "\n".join(parts)
