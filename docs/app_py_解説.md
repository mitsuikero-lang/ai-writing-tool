# app.py を読み解く — AIライティングツールの「司令塔」

## このファイルの役割

`app.py` はアプリ全体の**玄関口**です。ユーザーが最初に触れる画面の骨格がすべてここに書かれています。5つの機能（ブログ執筆・メール返信・要約・校正・SNS）は別ファイルに分かれていますが、`app.py` がそれらを束ねて呼び出す**司令塔**の役割を担っています。

---

## 1. 最初の準備：ライブラリの読み込みと .env の読み取り

```python
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
```

| コード | 意味 |
|---|---|
| `import os` | 環境変数（APIキー）を読み書きするOS機能を使うため |
| `import streamlit as st` | 画面を作るフレームワーク |
| `load_dotenv()` | `.env` ファイルを読み込み、中身を環境変数として使えるようにする |

`load_dotenv()` を呼ぶことで、`.env` に書いた `GEMINI_API_KEY=xxx` が `os.getenv("GEMINI_API_KEY")` で取得できるようになります。

---

## 2. ページ全体の設定

```python
st.set_page_config(
    page_title="AIライティングツール",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded",
)
```

ブラウザのタブに表示されるタイトルや、レイアウトをここで一括設定します。`layout="wide"` にするとコンテンツが画面幅いっぱいに広がり、`initial_sidebar_state="expanded"` でサイドバーが最初から開いた状態になります。

---

## 3. サイドバーの構成（3つのブロック）

```python
with st.sidebar:
    ...
```

`with st.sidebar:` の中に書いたものはすべて左のサイドバーに表示されます。中身は3つのブロックに分かれています。

### ブロック1：APIキー管理

```python
api_key_env = os.getenv("GEMINI_API_KEY", "")
if not api_key_env:
    api_key_input = st.text_input("Gemini APIキー", type="password", ...)
    if api_key_input:
        os.environ["GEMINI_API_KEY"] = api_key_input
else:
    st.success("APIキー設定済み")
```

`.env` にキーがあれば「設定済み」と表示。なければ入力欄を表示し、入力されたら `os.environ` に直接セットします。これにより `.env` なしでもブラウザからキーを入力して使えます。

### ブロック2：ツール選択

```python
selected = st.radio("ツール選択", ["ブログ記事執筆", "メール返信文作成", ...])
```

`st.radio` はラジオボタンです。ユーザーが選んだ値が `selected` という変数に入ります。これが後の「どの画面を表示するか」の判定に使われます。

### ブロック3：AIモデル選択

```python
model_name = st.selectbox("モデル", ["gemini-2.5-flash-lite", ...])
st.session_state["model_name"] = model_name
```

`st.selectbox` はドロップダウンです。選んだモデル名を `st.session_state` という**アプリ全体で共有できる辞書**に保存します。こうすることで `gemini_client.py` など別ファイルからも `st.session_state["model_name"]` で取り出せます。

---

## 4. APIキー未設定時のガード

```python
if not os.getenv("GEMINI_API_KEY"):
    st.warning("サイドバーにGemini APIキーを入力してください。")
    st.stop()
```

`st.stop()` はそこで**画面の描画を強制停止**する命令です。APIキーがなければ以降のコードは一切実行されず、ツール画面は表示されません。

---

## 5. ツールの振り分け（ルーティング）

```python
if selected == "ブログ記事執筆":
    from tools.blog_writer import render_blog_writer
    render_blog_writer()
elif selected == "メール返信文作成":
    ...
```

`selected` の値に応じて対応する関数を呼び出します。`import` がここに書かれているのは意図的で、**選ばれたときだけ読み込む**ことで起動を速くしています。各 `render_*()` 関数の中に、それぞれのツールのフォームと生成ロジックが入っています。

---

## 全体の流れ まとめ

```
アプリ起動
    |
    v
.env を読む
    |
    v
サイドバーを描く（APIキー確認 → ツール選択 → モデル選択）
    |
    v
APIキーがなければ stop
    |
    v
selected の値に応じて tools/ の関数を呼ぶ
    |
    v
各ツールの画面が表示される
```

`app.py` 自体はロジックをほぼ持たず、**画面の骨格と交通整理だけ**を担っています。機能ごとの詳細は `tools/` 配下に分離されているため、新しいツールを追加するときも `app.py` への変更は2行（ラジオリストへの追加と `elif` の追加）だけで済む設計です。
