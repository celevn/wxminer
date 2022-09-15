import streamlit as st

from wxminer.miner import WXBackupLoader, LocalLoader, Chat
from wxminer.pages import build_page
from wxminer.consts import SELF_ID_DEFAULT, SELF_NAME_DEFAULT


def show_chat_loader():
    st.markdown("---")
    st.header("🥩 导入数据")
    st.markdown("""
        两种输入方式：
        1. [WX Backup](http://wxbackup.imxfd.com) 导出上传（推荐）
        2. WX Miner 本地运行，读取解析 iTunes 备份文件（开发中）
    """)
    tab1, tab2 = st.tabs(["选项一：WX Backup 导出上传", "选项二：读取本地 iOS 备份"])
    with tab1:
        st.markdown("""
            > 1. 打开 WX Backup 导出的聊天文件夹
            > 2. 上传 `js` 子文件夹中的 `message.js` 文件
        """)
        st.file_uploader("上传 message.js 文件", type="js", key="file_uploaded")
    with tab2:
        if "backup_dir" in st.session_state:
            st.markdown("""
                > 1. 点击 `读取` 按钮
                > 2. 选择想要挖掘的聊天
            """)
        else:
            st.error("该功能仅支持本地版")

def show_chat_parser():
    st.markdown("---")
    st.header("👩‍🍳 解析数据")
    with st.form("parser"):
        with st.expander("补充本人信息"):
            # self_id = st.text_input("微信号", value=SELF_ID_DEFAULT, max_chars=20)
            self_name = st.text_input("你的微信昵称", value=SELF_NAME_DEFAULT, max_chars=20)
        button_parse = st.form_submit_button("开始解析")
    if button_parse:
        try:
            file = st.session_state["file_uploaded"]
            chat = parse_chat(file, self_id=None, self_name=self_name)
        except Exception as err:
            st.error(f"聊天记录解析失败: {err}")
        else:
            st.session_state["chat"] = chat
            st.success("聊天记录解析成功！")
            show_date_picker()

@st.experimental_memo
def parse_chat(message_file, self_id, self_name):
    loader = WXBackupLoader()
    chat = loader.load_chat(message_file, self_id=self_id, self_name=self_name)
    return chat

def show_date_picker():
    st.markdown("---")
    st.header("📅 选取时间")
    with st.form("datepicker"):
        min_date, max_date = st.session_state["chat"].get_date_span()
        sdate = st.date_input("请选择挖掘开始日期", min_date, key="sdate")
        edate = st.date_input("请选择挖掘结束日期", max_date, key="edate")
        button_date = st.form_submit_button("确认")
    if button_date:
        st.session_state["chat"].set_date_span(sdate, edate)
        st.success("时间选取成功！挖掘准备就绪，请到后续页面查看！")
        st.balloons()


body = build_page("WX Miner", "🍽", "数据准备", "向 WX Miner 投喂原料")
with body:
    show_chat_loader()
    if "chat" not in st.session_state:
        if st.session_state["file_uploaded"]:
            show_chat_parser()
    else:
        show_chat_parser()
        show_date_picker()
