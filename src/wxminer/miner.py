import datetime
import json

import pandas as pd

from .consts import (SELF_ID_DEFAULT, SELF_NAME_DEFAULT, SELF_HEADIMG_DEFAULT,
                     MESSAGE_TYPE, MESSAGE_TYPE_EXT)
from .utils import parse_xml_msg


class Loader:
    """load data from different sources"""
    def __init__(self) -> None:
        pass

    def clean_member(self):
        pass

    def clean_message(self):
        pass


class WXBackupLoader(Loader):
    """build Chat on WXBackup export"""
    def __init__(self) -> None:
        super().__init__()

    def load_chat(self, file):
        """
        Parse message.js file to build Chat

        Args:
            file: FileObject with open/read method

        Returns:
            chat: wxminer.miner.Chat
        """
        try:
            js = json.loads(file.read()[11:])
            type = js.get("type")
            member = self.clean_member(js.get("member"))
            message = self.clean_message(js.get("message"), member)
        except:
            raise
        else:
            return Chat(**{"type": type, "member": member, "message": message})

    def clean_member(self, member):
        """
        clean member names and head images
        """
        df_member = pd.DataFrame(member).T
        df_member = df_member.replace("", pd.NA).drop("").dropna(how="all")
        df_member = df_member[~df_member.index.str.endswith("chatroom")]
        name_split = (df_member["name"].str.replace("^[\x00-\x1f]+", "", regex=True)
                                       .str.split("[\x00-\x1f]+", expand=True))
        df_member["name"] = name_split[0]
        df_member["remark"] = "" if 1 not in name_split else name_split[1]
        df_member["headimg"] = df_member["head"].str.replace("[\x00-\x1f]", "", regex=True)
        df_member = df_member[["name", "remark", "headimg"]]
        df_member.loc[SELF_ID_DEFAULT] = [SELF_NAME_DEFAULT, "我", SELF_HEADIMG_DEFAULT]
        return df_member

    def clean_message(self, message, member):
        df_message = pd.DataFrame(message)
        df_message["svrid"] = df_message["m_uiMesSvrID"]
        df_message = df_message.sort_values("m_uiCreateTime")
        df_message["dt"] = (df_message["m_uiCreateTime"].apply(
            datetime.datetime.fromtimestamp, args=(datetime.timezone.utc,)
        ).dt.tz_convert("Asia/Shanghai"))

        idx_sysmsg = df_message["m_uiMessageType"]>=10000
        idx_selfmsg = df_message["m_nsToUsr"]!=""
        idx_appmsg = df_message["m_uiMessageType"]==49
        idx_videomsg = df_message["m_uiMessageType"]==43

        df_message[["sender", "content"]] = df_message[["m_nsRealChatUsr", "m_nsContent"]]
        
        # WXBackup 在拆分发送者与消息内容时存在错误，XML 格式的消息需要修正
        # 修正拆分错误
        idx_split_bug = df_message["m_nsRealChatUsr"].str.startswith("<")
        df_message.loc[idx_split_bug, "content"] = df_message["sender"] + df_message["content"]
        # 修正">"缺失
        idx_split_bad = df_message["m_nsRealChatUsr"] == "<msg"
        df_message.loc[idx_split_bad, "content"] = "<msg>" + df_message["content"]
        # 清空发送者错误
        df_message.loc[idx_split_bug, "sender"] = None

        # 标注本人消息
        df_message.loc[idx_selfmsg, "sender"] = SELF_ID_DEFAULT

        # 解析 appmsg 类型并标注
        df_message.loc[idx_appmsg, "appmsgType"] = (
            df_message[idx_appmsg]["content"].apply(parse_xml_msg, path="appmsg/type")
                                             .fillna(-1).astype(int)
        )
        idx_patmsg = df_message["appmsgType"] == 62
        idx_refermsg = df_message["appmsgType"] == 57

        # combine sender id hidden in xml
        df_message["sender"] = (df_message["sender"]
            .combine_first(df_message[idx_appmsg]["content"].apply(parse_xml_msg, path="fromusername"))
            .combine_first(df_message[idx_videomsg]["content"].apply(parse_xml_msg, path="videomsg", attr="fromusername"))
            .combine_first(df_message[idx_patmsg]["content"].apply(parse_xml_msg, path="appmsg/patMsg//fromUser"))
            .combine_first(df_message[idx_refermsg]["content"].apply(parse_xml_msg, path="appmsg/refermsg/chatusr"))
        )

        df_message["name"] = df_message["sender"].map(member["name"])
        df_message["type"] = df_message["m_uiMessageType"].map(MESSAGE_TYPE)
        df_message["type_ext"] = df_message["appmsgType"].map(MESSAGE_TYPE_EXT)

        columns = ["svrid", "dt", "sender", "name", "type", "type_ext", "content"]
        return df_message[columns]


class LocalLoader(Loader):
    """build Chat on local iOS backup"""
    def __init__(self) -> None:
        super().__init__()

    def parse_ios_backup(path=None):
        """
        Parse local iOS backup
        """
        pass


    def clean_member(member):
        """"""
        pass


    def clean_message(message):
        """"""
        pass


class Chat:
    """"""
    def __init__(self,
                 type : str,
                 member : pd.DataFrame,
                 message : pd.DataFrame,
                 selfname=SELF_NAME_DEFAULT) -> None:
        self.message = message
        self.member = member
        self.type = type
        self.selfname = selfname

    def get_date_span(self) -> tuple:
        min_date = self.message["dt"].min().date()
        max_date = self.message["dt"].max().date()
        return (min_date, max_date)

    def set_date_span(self, sdate="2000-01-01", edate="2099-01-01") -> None:
        sdate = sdate.strftime("%Y-%m-%d") if isinstance(sdate, datetime.date) else sdate
        edate = edate.strftime("%Y-%m-%d") if isinstance(edate, datetime.date) else edate
        self.sdate, self.edate = sdate, edate
        self.message = self.message[
            (self.message["dt"]>=self.sdate)
            &(self.message["dt"].dt.floor("D")<=self.edate)
        ]

    def calc_chat_stats(self) -> None:
        self.message_count = len(self.message)
        self.active_user_count = self.message["sender"].nunique()
        self.active_day_count = self.message["dt"].dt.date.nunique()
        message_last_day = self.message[self.message["dt"] > self.edate]
        self.message_count_last_day = len(message_last_day)
        self.active_user_count_last_day = message_last_day["sender"].nunique()

    def get_message_daily_count(self) -> pd.DataFrame:
        message_daily = (self.message.set_index("dt")
                                     .resample("D")["content"]
                                     .count().rename("message_count")
                                     .reset_index())
        message_daily["weekday"] = message_daily["dt"].dt.day_name()
        return message_daily

    def get_message_hourly_count(self) -> pd.DataFrame:
        message_hourly = (self.message.set_index("dt")
                                     .resample("H")["content"]
                                     .count().rename("message_count")
                                     .reset_index())
        message_hourly["hour"] = message_hourly["dt"].dt.hour
        return message_hourly

    def get_message_type_dist(self) -> pd.DataFrame:
        message_type = (self.message.groupby("type")["content"]
                                    .count().rename("message_count")
                                    .reset_index())
        return message_type

    def get_message_type_ext_dist(self) -> pd.DataFrame:
        message_type_ext = (self.message.groupby("type_ext")["content"]
                                        .count().rename("message_count")
                                        .reset_index())
        return message_type_ext

    def get_message_type_dist_tree(self) -> pd.DataFrame:
        message_type_tree = pd.concat([
            self.message.groupby("type")[["content"]].count().assign(parent="消息"),
            self.message.groupby("type_ext")[["content"]].count().assign(parent="应用消息"),
        ], axis=0)
        message_type_tree = message_type_tree.reset_index()
        message_type_tree.columns = ["type", "message_count", "parent"]
        return message_type_tree
