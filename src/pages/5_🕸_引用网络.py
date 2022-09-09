from math import log
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from pyvis.network import Network

from wxminer.utils import parse_xml_msg
from wxminer.pages import build_page


def show_refer_network(chat, topn=100):
    st.markdown("---")
    st.header("🔗 引用网络")
    st.caption("遥相望，引相谈，答疑问，救冷场")

    message, member = chat.message, chat.member
    message_refer = message[message["type_ext"]=="引用"][["svrid", "sender", "content"]].assign(
        svrid_r=lambda df: (df["content"].apply(
            parse_xml_msg, path="appmsg/refermsg/svrid"
        ).astype("Int64"))
    )
    message_refer = message_refer.join(
        message.set_index("svrid")["sender"], on="svrid_r", rsuffix="_r")
    message_refer_agg = (message_refer[["sender", "sender_r"]].value_counts()
                                                              .map(log).rename("value")
                                                              .nlargest(topn).reset_index())
    message_refer_agg["name"] = message_refer_agg["sender"].map(member["name"])
    message_refer_agg["name_r"] = message_refer_agg["sender_r"].map(member["name"])
    
    nodes = (pd.concat([message_refer_agg["sender"], message_refer_agg["sender_r"]], axis=0)
               .rename("size").value_counts().to_frame().join(member["name"]))
    # st.experimental_show(nodes)
    edges = message_refer_agg[["sender", "sender_r", "value"]].itertuples(index=False, name=None)
    net = Network(height="500px", width="100%")
    net.add_nodes(nodes.index, size=nodes["size"].map(float), label=nodes["name"], title=nodes["name"])
    net.add_edges(edges)
    components.html(net.generate_html(), height=600, scrolling=True)


body = build_page("WX Miner", "🕸", "引用网络", "关于那些隔空对白")
with body:
    if "chat" in st.session_state:
        chat = st.session_state["chat"]
        show_refer_network(chat)
    else:
        st.markdown("---")
        st.warning("请先完成数据准备")