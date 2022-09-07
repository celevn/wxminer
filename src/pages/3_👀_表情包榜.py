import streamlit as st
import pandas as pd

from wxminer.utils import parse_xml_msg
from wxminer.pages import build_page


def show_sticker_rank(chat, topn=10):
    st.markdown("---")
    st.header("🏅 斗战圣图")
    st.caption("滥用人数与滥用次数")

    message_sticker = chat.message[chat.message["type"] == "表情"].assign(
        url=lambda df: df["content"].apply(parse_xml_msg, path='emoji', attr='cdnurl')
    )
    sticker_agg = message_sticker.groupby("url").agg(
        user_count=pd.NamedAgg("sender", "nunique"),
        message_count=pd.NamedAgg("content", "count"),
    )
    sticker_rank = sticker_agg.reset_index().nlargest(topn, ["user_count", "message_count"])

    _, col, _ = st.columns(3)
    for i, gif in sticker_rank.iterrows():
        txt = "共 {} 人使用 {} 次".format(gif["user_count"], gif["message_count"])
        with col:
            st.image(gif["url"], width=200, caption=txt)

    # html = sticker_rank.to_html(
    #     index=False, escape=False, formatters={'url': lambda url: f'<img src="{url}" width="60">'}
    # )
    # st.write(html, unsafe_allow_html=True)


body = build_page("WX Miner", "👀", "表情包榜", "一图胜千言")
with body:
    if "chat" in st.session_state:
        chat = st.session_state["chat"]
        show_sticker_rank(chat)
    else:
        st.markdown("---")
        st.warning("请先完成数据准备")