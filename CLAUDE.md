# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 起動・開発コマンド

```powershell
# 依存パッケージのインストール
pip install -r requirements.txt

# アプリの起動
streamlit run app.py
```

## アーキテクチャ

Streamlit のシングルページアプリ。サイドバーのラジオボタンでツールを切り替え、選択に応じて `tools/` 配下の `render_*` 関数を呼び出す構成。

```
app.py                  # エントリーポイント。サイドバー（APIキー・ツール選択・モデル選択）と画面ルーティング
utils/gemini_client.py  # Gemini API の唯一の窓口。全ツールが generate_text() を呼び出す
tools/
  blog_writer.py        # ブログ記事執筆
  email_reply.py        # メール返信文作成
  summarizer.py         # 文章要約
  proofreader.py        # 文章校正・リライト
  sns_writer.py         # SNS投稿文作成（X / Instagram / Facebook / LinkedIn）
```

## 重要な設計ルール

**モデル選択の流れ：**
`app.py` のサイドバーで選んだモデル名が `st.session_state["model_name"]` に格納され、`generate_text()` がそれを参照する。デフォルトは `gemini-2.5-flash-lite`。

**新ツールの追加手順：**
1. `tools/` に `render_*()` 関数と `_build_prompt()` 関数を持つファイルを作成
2. `app.py` のサイドバーのラジオリストにラベルを追加
3. `app.py` 末尾の `if/elif` にルーティングを追加

**Gemini SDK：**
`google-generativeai`（廃止済み）ではなく `google-genai` を使用。クライアントは `@st.cache_resource` でキャッシュしているため、`api_key` が変わったときのみ再生成される。

## 環境変数

`.env.example` をコピーして `.env` を作成し `GEMINI_API_KEY` を設定する。APIキーは Google AI Studio（https://aistudio.google.com/apikey）で取得。Google Cloud の請求アカウント連携が必要。

## 利用可能なモデル（2025年5月時点）

`gemini-2.0-flash` 以前は新規ユーザー向けに廃止済み。`gemini-2.5-flash-lite` 以上を使うこと。
