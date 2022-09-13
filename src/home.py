import streamlit as st

from wxminer.pages import build_page


body = build_page()

with body:
    st.markdown("---")
    st.header("🐦 功能清单")
    st.markdown("""
        见左侧页面，下列功能规划中：

        - [x] 文本消息：词云展示、话题挖掘、情感分析...
        - [x] 引用消息：高引节点、对话网络...
        - [ ] 关联挖掘：关联亲密度、友爱晴雨表...
        - [ ] 本地运行：无上传限制、更快地挖掘...
    """)
    st.markdown("---")
    st.header("🧭 食用指南")
    st.markdown("""
        1. 准备手机：iPhone （或已导入微信聊天记录的 iPad），**不支持 Android**
        2. 准备电脑：macOS（或已安装 iTunes 的 Windows）
        3. 数据备份：将手机内容备份至电脑（[操作指引](https://support.apple.com/zh-cn/guide/iphone/iph3ecf67d29/ios)），请勿勾选`加密本地备份`
        4. 导出聊天：下载 [WX Backup](http://wxbackup.imxfd.com) 运行，导出想要挖掘的聊天
        5. 开始挖掘：进入 WX Miner 数据准备页，按提示操作即可
    """)
    st.markdown("---")
    st.header("🙈 隐私声明")
    st.markdown("""
        聊天记录属于个人隐私，请注意妥善保管。

        [WX Miner 代码开源](https://github.com/celevn/wxminer)，web app 公开托管于 [Streamlit Cloud](https://streamlit.io/cloud)。

        作为工具，WX Miner 尊重用户隐私，[不会也无法留存](https://docs.streamlit.io/knowledge-base/using-streamlit/where-file-uploader-store-when-deleted)用户上传的聊天记录，请安心食用。
    """)