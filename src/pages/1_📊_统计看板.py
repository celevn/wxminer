import streamlit as st
import plotly.express as px

from wxminer.pages import build_page


def show_chat_stats(chat):
    st.markdown("---")
    st.header("💯 关键聊天指标")
    st.caption("红色增长数字为挖掘期最后一日数目")
    try:
        chat.calc_chat_stats()
        col1, col2, col3 = st.columns(3)
        col1.metric(label="消息条数", delta_color="inverse",
                    value=chat.message_count, delta=chat.message_count_last_day)
        col2.metric(label="参与人数", delta_color="inverse",
                    value=chat.active_user_count, delta=chat.active_user_count_last_day)
        col3.metric(label="活跃天数", delta_color="inverse",
                    value=chat.active_day_count, delta=1)
    except Exception as err:
        st.error(f"出现了一点问题：{err}")

@st.experimental_memo
def plot_message_count(_chat):
    if (_chat.message["dt"].max() - _chat.message["dt"].min()).days > 730:
        message_count = _chat.get_message_monthly_count()
    else:
        message_count = _chat.get_message_daily_count()
    plotly_line_layout = {
        "xaxis_title": None,
        "yaxis_title": None,
        "showlegend": False,
        "margin": dict(t=25, l=25, r=25, b=25),
    }
    fig = px.line(message_count, x="dt", y="message_count").update_layout(plotly_line_layout)
    return fig

def show_message_count(chat):
    st.markdown("---")
    st.header("📈 消息数目曲线")
    st.caption("这消息跑得赢大盘吗")
    try:
        fig = plot_message_count(chat)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as err:
        st.error(f"出现了一点问题：{err}")

@st.experimental_memo
def plot_message_type_dist(_chat):
    treemap_data = _chat.get_message_type_dist_tree()
    fig = px.treemap(data_frame=treemap_data, values="message_count", names="type",
                     parents="parent", branchvalues="total")
    fig.update_traces({"textinfo": "value+label"})
    fig.update_layout({"margin": dict(t=25, l=25, r=25, b=25)})
    return fig

def show_message_type_dist(chat):
    st.markdown("---")
    st.header("🎨 消息类型分布")
    st.caption("点击拼图可以放大")
    try:
        fig = plot_message_type_dist(chat)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as err:
        st.error(f"出现了一点问题：{err}")

@st.experimental_memo
def plot_message_weekday_dist(_chat):
    message_count = _chat.get_message_daily_count()
    plotly_box_layout = {
        "xaxis_title": None,
        "yaxis_title": None,
        "showlegend": False,
        "margin": dict(t=25, l=25, r=25, b=25),
    }
    fig = px.box(message_count, x="weekday", y="message_count").update_layout(plotly_box_layout)
    return fig

def show_message_weekday_dist(chat):
    st.markdown("---")
    st.header("🧑‍💻 周内活跃度对比")
    st.caption("工作日勤勤恳恳摸鱼，休息日兢兢业业划水")
    try:
        fig = plot_message_weekday_dist(chat)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as err:
        st.error(f"出现了一点问题：{err}")

@st.experimental_memo
def plot_message_hour_dist(_chat):
    message_hourly = _chat.get_message_hourly_count()
    plotly_box_layout = {
        "xaxis_title": None,
        "yaxis_title": None,
        "showlegend": False,
        "margin": dict(t=25, l=25, r=25, b=25),
    }
    fig = px.box(message_hourly, x="hour", y="message_count").update_layout(plotly_box_layout)
    return fig

def show_message_hour_dist(chat):
    st.markdown("---")
    st.header("🌗 日内活跃度对比")
    st.caption("一日三餐分出两段白昼，嗨歌安睡亦是不同夜幕")
    try:
        fig = plot_message_hour_dist(chat)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as err:
        st.error(f"出现了一点问题：{err}")


body = build_page("WX Miner", "📊", "统计看板", "聊天大数据、活跃曲线、消息类型")
with body:
    if "chat" in st.session_state:
        chat = st.session_state["chat"]
        show_chat_stats(chat)
        show_message_count(chat)
        show_message_type_dist(chat)
        show_message_weekday_dist(chat)
        show_message_hour_dist(chat)
    else:
        st.markdown("---")
        st.warning("请先完成数据准备")