from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, model_serializer
from typing_extensions import override


class MsgType(Enum):
    """
    消息类型
    """

    TEXT = "text"
    LINK = "link"
    MARKDOWN = "markdown"
    ACTIONCARD = "actionCard"
    FEEDCARD = "feedCard"


class Message(ABC, BaseModel):
    """
    钉钉机器人发送的消息基类
    """

    @abstractmethod
    def msg_type() -> str:
        """
        返回消息类型字符串
        """
        raise NotImplementedError


class Text(Message):
    """
    文本类型消息
    """

    content: str  # 文本消息的内容

    @override
    def msg_type(self) -> str:
        return MsgType.TEXT.value


class Link(Message):
    """
    链接类型消息
    """

    title: str  # 链接消息标题
    text: str  # 链接消息的内容
    message_url: str = Field(alias="messageUrl")  # 点击消息跳转的链接
    pic_url: Optional[str] = Field(None, alias="picUrl")  # 链接消息内的图片地址，建议使用上传媒体文件接口获取

    @override
    def msg_type(self) -> str:
        return MsgType.LINK.value


class Markdown(Message):
    """
    markdwon 类型消息
    """

    title: str  # 消息会话列表中展示的标题，非消息体的标题
    text: str  # markdown 类型消息的文本内容

    @override
    def msg_type(self) -> str:
        return MsgType.MARKDOWN.value


class ActionCard(Message):
    """
    整体跳转 actionCard 类型消息
    """

    title: str  # 消息会话列表中展示的标题，非消息体的标题
    text: str  # actionCard 类型消息的正文内容，支持 markdown 语法
    single_title: Optional[str] = Field(None, alias="singleTitle")  # 按钮上显示的文本
    single_url: Optional[str] = Field(None, alias="singleURL")  # 点击 singleTitle 按钮触发的链接

    @override
    def msg_type(self) -> str:
        return MsgType.ACTIONCARD.value


class ActionCardBtn(BaseModel):
    """
    actionCard 类型消息的按钮
    """

    title: str  # 按钮上显示的文本
    action_url: str = Field(alias="actionURL")  # 按钮跳转的链接


class ActionsCard(Message):
    """
    独立跳转 actionCard 类型消息
    """

    title: str  # 消息会话列表中展示的标题，非消息体的标题
    text: str  # actionCard 类型消息的正文内容，支持 markdown 语法
    btns: Optional[List[ActionCardBtn]] = None  # 按钮的信息列表
    btn_orientation: Optional[str] = Field(None, alias="btnOrientation")  # 消息内按钮排列方式，0：按钮竖直排列，1：按钮横向排列

    @override
    def msg_type(self) -> str:
        return MsgType.ACTIONCARD.value


class FeedCardLink(BaseModel):
    """
    feedCard 类型消息的内容
    """

    title: str  # 每条内容的标题
    message_url: str = Field(alias="messageURL")  # 每条内容的跳转链接
    pic_url: str = Field(alias="picURL")  # 每条内容的图片链接，建议使用上传媒体文件接口获取


class FeedCard(Message):
    """
    feedCard 类型消息
    """

    links: List[FeedCardLink]  # feedCard 类型消息的内容列表

    @override
    def msg_type(self) -> str:
        return MsgType.FEEDCARD.value


class ErrorLayout(BaseModel):
    """
    错误类型消息卡片布局
    """

    header: str = ""  # 首行
    content: str = ""  # 内容
    footer: str = ""  # 页脚

    @model_serializer
    def __str__(self):
        return self.header + self.content + self.footer


class ErrorCard(Message):
    """
    错误类型消息
    """

    title: ErrorLayout  # 消息会话列表中展示的标题，非消息体的标题
    text: ErrorLayout  # actionCard 类型消息的正文内容，支持 markdown 语法
    single_title: Optional[str] = Field(None, alias="singleTitle")  # 按钮上显示的文本
    single_url: Optional[str] = Field(None, alias="singleURL")  # 点击 singleTitle 按钮触发的链接

    @override
    def msg_type(self) -> str:
        return MsgType.ACTIONCARD.value
