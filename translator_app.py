import streamlit as st
from googletrans import Translator
import pyperclip

st.set_page_config(page_title="🌸 翻譯小助手", page_icon="🌍")
st.title("🌸 我的翻譯小助手")
st.markdown("讓你隨時隨地 ✨ 快速翻譯 · 可愛又實用！")

translator = Translator()

lang_dict = {
    "中文（繁體）": "zh-TW",
    "英文": "en",
    "日文": "ja",
    "韓文": "ko",
    "法文": "fr",
    "德文": "de",
    "自動偵測": "auto"
}

col1, col2 = st.columns(2)
with col1:
    from_lang = st.selectbox("💬 輸入語言", list(lang_dict.keys()), index=6)
with col2:
    to_lang = st.selectbox("🌍 翻譯成", list(lang_dict.keys()), index=1)

text = st.text_area("✍️ 請輸入你想翻譯的文字")

if st.button("🚀 翻譯！"):
    if text.strip() == "":
        st.warning("請輸入文字喔！")
    else:
        from_code = lang_dict[from_lang]
        to_code = lang_dict[to_lang]
        result = translator.translate(text, src=from_code, dest=to_code)
        st.success("✅ 翻譯完成！")
        st.markdown("**📘 翻譯結果：**")
        st.code(result.text, language="")

        if st.button("📋 複製翻譯內容"):
            pyperclip.copy(result.text)
            st.toast("已複製到剪貼簿！", icon="✅")
