import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from wxminer.pages import build_page


def show_member_active_rank(chat, topn=10):
    st.markdown("---")
    st.header("🏇 活跃榜")
    st.caption("撑起群消息数半边天的废话大师 or 坚持日常出勤视察工作的领导")

    message = chat.message.assign(date=chat.message["dt"].dt.date)
    member_rank = message.groupby("sender").agg(**{
        "message_count": pd.NamedAgg("content", "count"),
        "active_days": pd.NamedAgg("date", "nunique"),
    }).nlargest(topn, ["message_count", "active_days"]).iloc[::-1]
    member_rank = member_rank.join(chat.member).reset_index()

    idx, data1, data2 = member_rank["name"], member_rank["message_count"], member_rank["active_days"]
    fig = go.Figure(
        data=[
            go.Bar(y=idx, x=data1, name="消息总数", orientation="h", xaxis="x", yaxis="y"),
            go.Bar(y=idx, x=data2, name="活跃天数", orientation="h", xaxis="x2", yaxis="y"),
        ],
        layout=go.Layout({
            "xaxis": {
                "domain": [0, 0.5],
                "autorange": "reversed",
            },
            "xaxis2": {
                "domain": [0.5, 1],
            },
            "legend": {
                "orientation": "h",
                "x": 0.5, "xanchor": "center",
            },
            "margin": dict(t=25, l=25, r=25, b=25),
        })
    )
    st.plotly_chart(fig, use_container_width=True)


def show_member_recall_rank(chat, topn=10):
    st.markdown("---")
    st.header("␀ 撤回榜")
    st.caption("又撤回了什么见不得人的消息")

    message_recall = chat.message[
        (chat.message["type"] == "系统消息") & (chat.message["content"].str.contains("撤回"))
    ]
    recall_rank = (message_recall["content"].str.extract("\"(.*?)\"")[0]
                                            .value_counts()
                                            .rename_axis("name")
                                            .rename("recall_count")
                                            .head(topn))
    _, col, _ = st.columns([1,2,1])
    with col:
        for name, recalls in recall_rank.items():
            st.caption(f"`{name}` 撤回了 **`{recalls}`** 条消息")


def show_member_stayup_rank(chat, topn=10):
    st.markdown("---")
    st.header("🌜 熬夜榜")
    st.caption("月亮不睡我不睡")
    stayup_hours = st.slider("晚睡阈值", 0, 6, (0,6))
    
    message = chat.message.assign(date=chat.message["dt"].dt.date)
    message_stayup = message[(message["dt"].dt.hour >= stayup_hours[0])&
                             (message["dt"].dt.hour < stayup_hours[1])]
    member_stayup_monthly = message_stayup.groupby("sender").apply(
        lambda g: g.set_index("dt").rename_axis("month").resample("MS").agg(**{
            "stayup_days": pd.NamedAgg("date", "nunique"),
            "stayup_messages": pd.NamedAgg("content", "count"),
        })
    ).reset_index().join(chat.member, on="sender")
    member_stayup_rank = (member_stayup_monthly.groupby(["sender", "name"]).sum()
                                               .nlargest(topn, ["stayup_days", "stayup_messages"])
                                               .reset_index())
    plotly_scatter_layout = {
        "xaxis_title": None,
        "yaxis_title": None,
        "showlegend": False,
        "margin": dict(t=25, l=25, r=25, b=25),
    }
    data = member_stayup_monthly[member_stayup_monthly["sender"].isin(member_stayup_rank["sender"])]
    fig = px.scatter(
        data_frame=data, x="month", y="name",
        color="stayup_days", size="stayup_messages",
        color_continuous_scale="ice_r",
    ).update_traces(
        marker_symbol="star-diamond",
    ).update_layout(
        yaxis_categoryorder="array",
        yaxis_categoryarray=member_stayup_rank["name"][::-1],
    ).update_layout(plotly_scatter_layout)
    st.plotly_chart(fig, use_container_width=True)


def show_battle_of_two(chat):
    st.markdown("---")
    st.header("🤼‍♀️ 两人掰头")
    st.caption("...俩人有啥好比的🤣")


body = build_page("WX Miner", "🏆", "好友比拼", "刁钻奖杯，花落谁家")
with body:
    if "chat" in st.session_state:
        chat = st.session_state["chat"]
        if chat.type == "group":
            show_member_active_rank(chat)
            show_member_recall_rank(chat)
            show_member_stayup_rank(chat)
        else:
            show_battle_of_two(chat)
    else:
        st.markdown("---")
        st.warning("请先完成数据准备")