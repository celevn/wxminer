import streamlit as st
import pandas as pd

from wxminer.utils import parse_xml_msg
from wxminer.pages import build_page


@st.experimental_memo
def get_sticker_rank(_chat, topn):
    message = _chat.message
    message_sticker = message[message["type"] == "表情"].assign(
        url=lambda df: df["content"].apply(parse_xml_msg, path='emoji', attr='cdnurl')
    )
    sticker_agg = message_sticker.groupby("url").agg(
        user_count=pd.NamedAgg("sender", "nunique"),
        message_count=pd.NamedAgg("content", "count"),
    )
    sticker_rank = sticker_agg.reset_index().nlargest(topn, ["user_count", "message_count"])
    return sticker_rank

def show_sticker_rank(chat, topn=10):
    st.markdown("---")
    st.header("🏅 斗战圣图")
    st.caption("一图胜千言")
    sticker_rank = get_sticker_rank(chat, topn)
    _, col, _ = st.columns(3)
    for i, gif in sticker_rank.iterrows():
        txt = "共 {} 人使用 {} 次".format(gif["user_count"], gif["message_count"])
        with col:
            st.image(gif["url"], width=200, caption=txt)


body = build_page("WX Miner", "👀", "表情包榜", "据说每个聊天框都有属于自己的表情包语言")
with body:
    if "chat" in st.session_state:
        chat = st.session_state["chat"]
        try:
            show_sticker_rank(chat)
        except Exception as err:
            st.error(f"出现了一点问题：{err}")
    else:
        st.markdown("---")
        st.warning("请先完成数据准备")