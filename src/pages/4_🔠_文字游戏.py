import platform

import streamlit as st
import pandas as pd
from wordcloud import WordCloud

try:
    import jieba_fast as jieba
except ModuleNotFoundError:
    import jieba

from wxminer.utils import parse_xml_msg
from wxminer.pages import build_page


@st.experimental_memo
def get_stopwords():
    url_template = "https://raw.githubusercontent.com/goto456/stopwords/master/{}_stopwords.txt"
    stopwords = set(pd.concat([
        pd.read_csv(url_template.format(prefix), header=None, on_bad_lines="skip", quoting=3)
        for prefix in ["cn", "baidu", "hit", "scu"]
    ]))
    return stopwords


@st.experimental_memo
def get_chat_word(_chat, topn=100):
    message = _chat.message
    text = pd.concat([
        message[message["type"]=="文本"]["content"],
        message[message["type_ext"]=="引用"]["content"].apply(parse_xml_msg, path="appmsg/title"),
    ])
    stopwords = get_stopwords()
    word_freq = (text.map(lambda s: set(jieba.cut(s))-stopwords, na_action="ignore")
                     .explode().value_counts())
    word_freq = word_freq[word_freq.index.str.len()>1].head(topn)
    return word_freq


def plot_word_cloud(word_freq):
    font_by_os = {
        "Linux": "wqy-zenhei",
        "Windows": "Simhei",
        "Darwin": "STHeiti Medium",
    }
    font = font_by_os.get(platform.system(), None)

    wc = WordCloud(font_path=font, width=600, height=400, mode="RGBA", background_color=None)
    fig = wc.generate_from_frequencies(word_freq).to_image()
    st.image(fig, use_column_width=True)


def show_word_cloud(chat):
    st.markdown("---")
    st.header("聊天词云")
    st.caption("词不起眼，重要的是其背后所藏故事")
    word_freq = get_chat_word(chat)
    plot_word_cloud(word_freq)


body = build_page("WX Miner", "🔠", "文字游戏", "一切都在言语中")
with body:
    if "chat" in st.session_state:
        chat = st.session_state["chat"]
        try:
            show_word_cloud(chat)
        except Exception as err:
            st.error(f"出现了一点问题：{err}")
    else:
        st.markdown("---")
        st.warning("请先完成数据准备")
