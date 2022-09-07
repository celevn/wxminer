import streamlit as st
import plotly.express as px

from wxminer.pages import build_page


def show_chat_stats(chat):
    st.markdown("---")
    st.header("💯 关键聊天指标")
    chat.calc_chat_stats()

    col1, col2, col3 = st.columns(3)
    col1.metric(label="消息条数", delta_color="inverse",
                value=chat.message_count, delta=chat.message_count_last_day)
    col2.metric(label="参与人数", delta_color="inverse",
                value=chat.active_user_count, delta=chat.active_user_count_last_day)
    col3.metric(label="活跃天数", delta_color="inverse",
                value=chat.active_day_count, delta=1)

def show_message_daily(chat):
    st.markdown("---")
    st.header("📈 逐日消息数目")
    message_daily = chat.get_message_daily_count()

    plotly_line_layout = {
        "xaxis_title": None,
        "yaxis_title": None,
        "showlegend": False,
        "margin": dict(t=25, l=25, r=25, b=25),
    }
    fig = px.line(message_daily, x="dt", y="message_count").update_layout(plotly_line_layout)
    st.plotly_chart(fig, use_container_width=True)

def show_message_type_dist(chat):
    st.markdown("---")
    st.header("🎨 消息类型分布")
    st.caption("点击拼图可以放大")
    treemap_data = chat.get_message_type_dist_tree()

    fig = px.treemap(data_frame=treemap_data, values="message_count", names="type",
                     parents="parent", branchvalues="total")
    fig.update_traces({"textinfo": "value+label"})
    fig.update_layout({"margin": dict(t=25, l=25, r=25, b=25)})
    st.plotly_chart(fig, use_container_width=True)

def show_message_weekday_dist(chat):
    st.markdown("---")
    st.header("🧑‍💻 周内活跃度对比")
    st.caption("工作日勤勤恳恳摸鱼，休息日兢兢业业划水")
    message_daily = chat.get_message_daily_count()

    plotly_box_layout = {
        "xaxis_title": None,
        "yaxis_title": None,
        "showlegend": False,
        "margin": dict(t=25, l=25, r=25, b=25),
    }
    fig = px.box(message_daily, x="weekday", y="message_count").update_layout(plotly_box_layout)
    st.plotly_chart(fig, use_container_width=True)

def show_message_hour_dist(chat):
    st.markdown("---")
    st.header("🌗 日内活跃度对比")
    st.caption("一日三餐分出两段白昼，嗨歌安睡亦是不同夜幕")
    message_hourly = chat.get_message_hourly_count()

    plotly_box_layout = {
        "xaxis_title": None,
        "yaxis_title": None,
        "showlegend": False,
        "margin": dict(t=25, l=25, r=25, b=25),
    }
    fig = px.box(message_hourly, x="hour", y="message_count").update_layout(plotly_box_layout)
    st.plotly_chart(fig, use_container_width=True)


body = build_page("WX Miner", "📊", "统计看板", "聊天大数据、活跃曲线、消息类型")
with body:
    if "chat" in st.session_state:
        chat = st.session_state["chat"]
        show_chat_stats(chat)
        show_message_daily(chat)
        show_message_type_dist(chat)
        show_message_weekday_dist(chat)
        show_message_hour_dist(chat)
    else:
        st.markdown("---")
        st.warning("请先完成数据准备")