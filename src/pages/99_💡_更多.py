import streamlit as st

from wxminer.pages import build_page


body = build_page()

with body:
    st.markdown("---")
    st.header("参与共建")
    st.markdown("""
        💡 使用问题？想法建议？拓展开发？

        1. 到 [GitHub](https://github.com/celevn/wxminer/issues) 新建 Issue
        2. 加入[交流群](https://raw.githubusercontent.com/celevn/wxminer/main/src/assets/QR_GROUP.JPG)一起讨论

        😋 觉得 WX Miner 有趣有用？

        1. 分享给你的朋友
        2. [请作者喝咖啡](https://raw.githubusercontent.com/celevn/wxminer/main/src/assets/QR_DONATE.PNG)
    """)
    st.markdown("---")
    st.header("引用致谢")
    st.markdown("""
        1. [Streamlit](https://streamlit.io)，以更快的方式开发和分享 data apps
        2. [WX Backup](http://wxbackup.imxfd.com)，导出及备份你的微信聊天记录
    """)