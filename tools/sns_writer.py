import streamlit as st
from utils.gemini_client import generate_text


def render_sns_writer():
    st.header("SNS投稿文作成")
    st.caption("テーマや内容を入力すると、各SNSに最適化された投稿文を生成します。")

    with st.form("sns_form"):
        topic = st.text_area(
            "投稿したいテーマ・内容 *",
            placeholder="例：新しいカフェに行ってきました。内装がおしゃれで、コーヒーが美味しかったです。",
            height=120,
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            platforms = st.multiselect(
                "プラットフォーム *",
                ["X (Twitter)", "Instagram", "Facebook", "LinkedIn"],
                default=["X (Twitter)", "Instagram"],
            )
        with col2:
            tone = st.selectbox(
                "トーン",
                [
                    "カジュアル・親しみやすい",
                    "フォーマル・プロフェッショナル",
                    "ユーモア・面白い",
                    "感情的・共感的",
                    "情報提供・教育的",
                ],
            )
        with col3:
            hashtag_count = st.slider("ハッシュタグ数", 0, 10, 3)

        col4, col5 = st.columns(2)
        with col4:
            include_emoji = st.checkbox("絵文字を含める", value=True)
        with col5:
            variations = st.slider("バリエーション数", 1, 3, 1)

        cta = st.text_input(
            "CTA・行動喚起（任意）",
            placeholder="例：フォローよろしくお願いします！ / コメントで教えてください！",
        )

        submitted = st.form_submit_button(
            "投稿文を生成", type="primary", use_container_width=True
        )

    if submitted:
        if not topic:
            st.error("投稿したいテーマ・内容を入力してください。")
            return
        if not platforms:
            st.error("プラットフォームを1つ以上選択してください。")
            return

        with st.spinner("投稿文を生成中..."):
            prompt = _build_prompt(
                topic, platforms, tone, hashtag_count, include_emoji, cta, variations
            )
            try:
                result = generate_text(prompt, temperature=0.9)
                st.success("生成完了！")
                st.markdown("---")
                st.subheader("生成された投稿文")
                st.markdown(result)

                st.download_button(
                    "投稿文をダウンロード",
                    result,
                    file_name="sns_posts.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")


def _build_prompt(topic, platforms, tone, hashtag_count, include_emoji, cta, variations):
    platform_str = "、".join(platforms)
    emoji_text = "適切な絵文字を含めてください。" if include_emoji else "絵文字は使わないでください。"
    cta_text = f'最後にCTAとして「{cta}」を自然に含めてください。' if cta else ""
    variation_text = (
        f"各プラットフォームにつき{variations}パターンのバリエーションを作成してください。"
        if variations > 1
        else ""
    )

    platform_notes = {
        "X (Twitter)": "X(Twitter)は140字以内（日本語）",
        "Instagram": "Instagramは魅力的なキャプション形式、改行を効果的に使用",
        "Facebook": "Facebookは少し長めでも可、親しみやすいトーン",
        "LinkedIn": "LinkedInはプロフェッショナルなトーン、業界に関連した視点",
    }
    notes = "、".join([platform_notes[p] for p in platforms if p in platform_notes])

    return f"""以下の内容でSNS投稿文を作成してください。

【投稿内容・テーマ】
{topic}

【条件】
プラットフォーム: {platform_str}
トーン: {tone}
ハッシュタグ数: {hashtag_count}個
{emoji_text}
{cta_text}
{variation_text}

【プラットフォーム別の注意点】
{notes}

各プラットフォームのセクションをマークダウンの見出し（##）で区切って出力してください。"""
