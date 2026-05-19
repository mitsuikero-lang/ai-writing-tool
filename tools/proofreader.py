import streamlit as st
from utils.gemini_client import generate_text


def render_proofreader():
    st.header("文章校正・リライト")
    st.caption("文章を入力すると、誤字脱字の修正や表現の改善を行います。")

    with st.form("proofreader_form"):
        text = st.text_area(
            "校正したい文章 *",
            placeholder="ここに校正・リライトしたいテキストを入力してください...",
            height=200,
        )

        col1, col2 = st.columns(2)
        with col1:
            mode = st.selectbox(
                "校正モード",
                [
                    "誤字脱字・文法チェック",
                    "読みやすさの改善",
                    "フォーマルに書き換え",
                    "カジュアルに書き換え",
                    "より簡潔に書き換え",
                    "より詳しく書き換え",
                    "完全リライト（内容保持）",
                ],
            )
        with col2:
            show_diff = st.checkbox("変更箇所を説明する", value=True)
            preserve_tone = st.checkbox("元の文体・トーンを保持", value=True)

        additional = st.text_area(
            "追加の指示（任意）",
            placeholder="例：専門用語はそのままにしてください。敬語を使ってください。",
            height=60,
        )

        submitted = st.form_submit_button(
            "校正・リライトする", type="primary", use_container_width=True
        )

    if submitted:
        if not text:
            st.error("校正したい文章を入力してください。")
            return

        with st.spinner("校正中..."):
            prompt = _build_prompt(text, mode, show_diff, preserve_tone, additional)
            try:
                result = generate_text(prompt, temperature=0.4)
                st.success("校正完了！")
                st.markdown("---")

                if show_diff:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("元の文章")
                        st.markdown(
                            f'<div style="background:#fff3cd;padding:1rem;'
                            f'border-radius:8px;border:1px solid #ffc107;">{text}</div>',
                            unsafe_allow_html=True,
                        )
                    with col2:
                        st.subheader("校正後")
                        st.markdown(result)
                else:
                    st.subheader("校正後の文章")
                    st.markdown(result)

                st.download_button(
                    "校正結果をダウンロード",
                    result,
                    file_name="proofread.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")


def _build_prompt(text, mode, show_diff, preserve_tone, additional):
    parts = [
        "以下の文章を校正・修正してください。",
        "",
        "【対象テキスト】",
        text,
        "",
        f"【校正モード】: {mode}",
    ]
    if preserve_tone:
        parts.append("元の文体・トーンはできるだけ保持してください。")
    if additional:
        parts.append(f"追加の指示: {additional}")

    if show_diff:
        parts += [
            "",
            "以下の形式で出力してください：",
            "## 校正後の文章",
            "（修正した文章をここに記述）",
            "",
            "## 変更点",
            "（何をどのように変更したかを箇条書きで説明）",
        ]
    else:
        parts.append("\n修正後の文章のみを出力してください（説明は不要）。")

    return "\n".join(parts)
