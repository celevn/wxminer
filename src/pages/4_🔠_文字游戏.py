import streamlit as st
import pandas as pd

from wxminer.pages import build_page


def show_word_cloud(chat):
    st.markdown("---")
    st.header("聊天词云")
    st.caption("词不起眼，重要的是其背后所藏故事")


body = build_page("WX Miner", "🔠", "文字游戏", "一切都在言语中")
with body:
    if "chat" in st.session_state:
        chat = st.session_state["chat"]
        show_word_cloud(chat)
    else:
        st.markdown("---")
        st.warning("请先完成数据准备")
