import streamlit as st
import re
from pykakasi import kakasi

kks = kakasi()

def to_hiragana(text):
    result = kks.convert(text)
    return ''.join([item['hira'] for item in result])

PLACEHOLDER = " ？？？ "

if "initialized" not in st.session_state:
    st.session_state.initialized = False

st.title("穴埋めクイズ")

if not st.session_state.initialized:
    text = st.text_area("半角[]で隠して入力")
    if st.button("スタート"):
        st.session_state.original = text
        st.session_state.answers = re.findall(r'[([^]]+)]', text)
        st.session_state.display = re.sub(r"[(.*?)]", PLACEHOLDER, text)
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.initialized = True
        st.rerun()

else:
    st.write(st.session_state.display)

    if st.session_state.index < len(st.session_state.answers):
        user_input = st.text_input("答えを入力", key="input")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("回答"):
                correct = st.session_state.answers[st.session_state.index]

                if to_hiragana(user_input) == to_hiragana(correct):
                    st.success("正解")
                    o = st.session_state.display.find(PLACEHOLDER)
                    if o != -1:
                        st.session_state.display = (
                            st.session_state.display[:o]
                            + correct
                            + st.session_state.display[o + len(PLACEHOLDER):]
                        )
                    st.session_state.score += 1
                    st.session_state.index += 1
                    st.rerun()
                else:
                    st.error("不正解")

        with col2:
            if st.button("降参するンゴ"):
                correct = st.session_state.answers[st.session_state.index]
                o = st.session_state.display.find(PLACEHOLDER)
                if o != -1:
                    st.session_state.display = (
                        st.session_state.display[:o]
                        + f"<{correct}>"
                        + st.session_state.display[o + len(PLACEHOLDER):]
                    )
                st.session_state.index += 1
                st.rerun()

    else:
        st.success(f" {len(st.session_state.answers)}問中 {st.session_state.score}問正解")
        st.write(st.session_state.display)

        if st.button("もう一度"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
