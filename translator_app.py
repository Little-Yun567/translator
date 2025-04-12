
import streamlit as st
from googletrans import Translator
from gtts import gTTS
import base64
import io

st.set_page_config(page_title="翻譯小助手 2.0", page_icon="🌸", layout="centered")

# ---------------- UI 樣式設定 ----------------
st.markdown("""
    <style>
    html, body {
        background-color: #fffaf3;
    }
    .title {
        font-size: 2.2em;
        color: #ff928b;
        text-align: center;
        margin-bottom: 0.5em;
    }
    .subtitle {
        font-size: 1em;
        color: #888888;
        text-align: center;
        margin-bottom: 2em;
    }
    .stTextArea textarea {
        background-color: #fff;
        border: 2px solid #ffcab4;
        border-radius: 1rem;
        padding: 1em;
    }
    .stButton button {
        border-radius: 1.5rem;
        background-color: #ffcab4;
        border: none;
        padding: 0.6em 1.5em;
        color: #fff;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #ffa58d;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- 翻譯邏輯 ----------------
translator = Translator()
if "history" not in st.session_state:
    st.session_state["history"] = []

st.markdown('<div class="title">🌸 翻譯小助手 2.0</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">可愛・實用・支援語音的翻譯 App！</div>', unsafe_allow_html=True)

text = st.text_area("輸入文字", height=150, key="input_text")
target_lang = st.selectbox("選擇翻譯語言", ["英文", "中文"], index=0)
lang_code = "en" if target_lang == "英文" else "zh-tw"

translated_text = ""
if text:
    translated = translator.translate(text, dest=lang_code)
    translated_text = translated.text

    st.markdown("#### 🎯 翻譯結果")
    st.success(translated_text)

    # 加入翻譯紀錄
    st.session_state["history"].insert(0, (text, translated_text))
    st.session_state["history"] = st.session_state["history"][:5]  # 保留前 5 筆

    # 一鍵複製功能
    st.code(translated_text, language="")
    st.download_button("📋 複製翻譯結果", translated_text, file_name="translation.txt")

    # 語音播放功能
    with st.spinner("🔊 產生語音中..."):
        tts = gTTS(translated_text, lang="en" if lang_code == "en" else "zh-tw")
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        audio_bytes = buf.read()
        b64 = base64.b64encode(audio_bytes).decode()
        audio_html = f'<audio autoplay controls src="data:audio/mp3;base64,{b64}"></audio>'
        st.markdown(audio_html, unsafe_allow_html=True)

# 顯示翻譯紀錄
if st.session_state["history"]:
    st.markdown("#### 📝 最近翻譯紀錄")
    for i, (original, result) in enumerate(st.session_state["history"], 1):
        st.markdown(f"**{i}.** {original} → _{result}_")
