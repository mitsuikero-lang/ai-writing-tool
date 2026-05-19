import streamlit as st
from utils.gemini_client import generate_text


def render_email_reply():
    st.header("メール返信文作成")
    st.caption("受信したメールの内容と返信の方向性を入力すると、適切な返信文を生成します。")

    with st.form("email_form"):
        received_email = st.text_area(
            "受信したメールの内容 *",
            placeholder="ここに受信したメールの内容を貼り付けてください...",
            height=200,
        )

        col1, col2 = st.columns(2)
        with col1:
            reply_type = st.selectbox(
                "返信の方向性",
                ["承諾・了解", "丁寧に断る", "質問・確認", "感謝・お礼", "詫び・謝罪", "情報提供"],
            )
            tone = st.selectbox(
                "トーン",
                ["フォーマル（ビジネス）", "セミフォーマル", "カジュアル（友人・知人）"],
            )
        with col2:
            language = st.selectbox(
                "言語",
                ["日本語", "英語", "日英両方"],
            )
            your_name = st.text_input(
                "差出人名（任意）",
                placeholder="例：田中太郎",
            )

        key_points = st.text_area(
            "返信で伝えたいポイント（任意）",
            placeholder="例：来週月曜日は参加可能です。会議室はAルームをお願いします。",
            height=80,
        )

        submitted = st.form_submit_button(
            "返信文を生成", type="primary", use_container_width=True
        )

    if submitted:
        if not received_email:
            st.error("受信したメールの内容を入力してください。")
            return

        with st.spinner("返信文を生成中..."):
            prompt = _build_prompt(
                received_email, reply_type, tone, language, your_name, key_points
            )
            try:
                result = generate_text(prompt, temperature=0.6)
                st.success("生成完了！")
                st.markdown("---")
                st.subheader("生成された返信文")
                st.text_area(
                    "返信文（コピーしてお使いください）",
                    result,
                    height=300,
                )
                st.download_button(
                    "テキストでダウンロード",
                    result,
                    file_name="email_reply.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")


def _build_prompt(received_email, reply_type, tone, language, your_name, key_points):
    parts = [
        "以下のメールへの返信文を作成してください。",
        "",
        "【受信メール】",
        received_email,
        "",
        "【返信の条件】",
        f"返信の方向性: {reply_type}",
        f"トーン・スタイル: {tone}",
        f"言語: {language}",
    ]
    if your_name:
        parts.append(f"差出人名: {your_name}")
    if key_points:
        parts.append(f"必ず含めるポイント: {key_points}")

    parts += [
        "",
        "件名から本文まで完全な返信メールを作成してください。",
        "自然で読みやすい文章にしてください。",
    ]
    return "\n".join(parts)
