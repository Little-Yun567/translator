import streamlit as st
from googletrans import Translator
from gtts import gTTS
import base64
import io

st.set_page_config(page_title="翻譯小助手 2.1", page_icon="🌸", layout="centered")

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

st.markdown('<div class="title">🌸 翻譯小助手 2.1</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">可愛・實用・支援多語言與語音播放的翻譯 App！</div>', unsafe_allow_html=True)

# 使用者輸入
text = st.text_area("輸入文字", height=150, key="input_text")

# 支援語言
LANGUAGES = {
    "英文": "en",
    "中文": "zh-tw",
    "日文": "ja",
    "韓文": "ko",
    "法文": "fr",
    "德文": "de",
    "西班牙文": "es",
    "泰文": "th",
    "越南文": "vi"
}

target_lang = st.selectbox("選擇翻譯語言", list(LANGUAGES.keys()), index=0)
lang_code = LANGUAGES[target_lang]

# 按鈕觸發翻譯
if st.button("✨ 開始翻譯"):
    if text.strip() == "":
        st.warning("請先輸入要翻譯的文字喔～")
    else:
        translated = translator.translate(text, dest=lang_code)
        translated_text = translated.text

        st.markdown("#### 🎯 翻譯結果")
        st.success(translated_text)

        # 紀錄翻譯歷史
        st.session_state["history"].insert(0, (text, translated_text))
        st.session_state["history"] = st.session_state["history"][:5]

        # 一鍵複製
        st.code(translated_text, language="")
        st.download_button("📋 複製翻譯結果", translated_text, file_name="translation.txt")

        # 語音播放
        with st.spinner("🔊 產生語音中..."):
            tts = gTTS(translated_text, lang=lang_code)
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

