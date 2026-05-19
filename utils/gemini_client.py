import os
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()


@st.cache_resource
def _get_client(api_key: str) -> genai.Client:
    return genai.Client(api_key=api_key)


def generate_text(prompt: str, temperature: float = 0.7) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY が設定されていません。サイドバーでAPIキーを入力するか、.envファイルを作成してください。")

    model_name = st.session_state.get("model_name", "gemini-2.5-flash-lite")
    client = _get_client(api_key)

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=temperature),
    )
    return response.text
