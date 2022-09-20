import streamlit as st
from streamlit_ace import st_ace

from wxminer.utils import parse_xml_msg
from wxminer.pages import build_page


default = """
# Write costom code here

# Notes:
# 1. remember to import needed modules e.g. `import pandas as pd`
# 2. use st.write() instead of print() to display/debug
# 3. correct your syntax error before running

st.dataframe(message.sample(20))
"""

def show_custom_runner():
    st.markdown("---")
    st.header("编写代码")
    code = st_ace(value=default, language="python")
    st.markdown("---")
    st.header("执行结果")
    exec(code)


body = build_page("WX Miner", "🐍", "自定义挖掘", "九块九的 Python 课有用了！")
with body:
    if "chat" in st.session_state:
        chat = st.session_state["chat"]
        message = chat.message
        try:
            show_custom_runner()
        except Exception as err:
            st.error(f"出现了一点问题：{err}")
    else:
        st.markdown("---")
        st.warning("请先完成数据准备")