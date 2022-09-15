import streamlit as st

from wxminer.pages import build_page, QR_GROUP_URL, QR_DONATE_URL


body = build_page()

with body:
    st.markdown("---")
    st.header("参与共建")

    st.subheader("💡 使用问题？想法建议？拓展开发？")
    with st.expander("1. 提交问题报告"):
        st.markdown("[New issue on GitHub](https://github.com/celevn/wxminer/issues/new)")
    with st.expander("2. 加交流群讨论"):
        st.image(QR_GROUP_URL)

    st.subheader("😋 觉得 WX Miner 有趣有用？")
    with st.expander("1. 分享给朋友们"):
        st.markdown("""
            - 使用链接：`https://share.streamlit.io/celevn/wxminer/main/src/home.py`
            - 录屏分享：右上角菜单 - `Record a screencast`
        """)
    with st.expander("2. 请作者喝咖啡"):
        st.image(QR_DONATE_URL)
    
    st.markdown("---")
    st.header("引用致谢")
    st.markdown("""
        1. [Streamlit](https://streamlit.io)，以更快的方式开发和分享 data apps
        2. [WX Backup](http://wxbackup.imxfd.com)，导出及备份你的微信聊天记录
    """)