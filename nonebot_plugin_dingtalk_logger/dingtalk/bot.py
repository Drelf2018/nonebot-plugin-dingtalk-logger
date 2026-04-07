from datetime import datetime
from typing import List, Optional

from loguru._handler import Message as LoguruMessage
from loguru._recattrs import RecordLevel
from pydantic import BaseModel, Field

from .api import At, generate_sign, send
from .models import (
    ActionCard,
    ActionCardBtn,
    ActionsCard,
    ErrorCard,
    ErrorLayout,
    FeedCard,
    FeedCardLink,
    Link,
    Markdown,
    Message,
    Text,
)


class SendResponse(BaseModel):
    """
    发送消息的响应体
    """

    msg: str = Field(alias="errmsg")
    code: int = Field(alias="errcode")


class Bot(BaseModel):
    """
    钉钉机器人
    """

    token: str = Field(alias="dingtalk_token")
    """调用接口的凭证，钉钉提供的 Webhook 链接中 access_token 的值"""

    secret: str = Field(default="", alias="dingtalk_secret")
    """安全密钥，创建机器人时在安全设置项选择了加签后，钉钉提供的 SEC 开头的字符串"""

    keywords: List[str] = Field(default_factory=list, alias="dingtalk_keywords")
    """自定义关键词，创建机器人时在安全设置项填入的所有关键词"""

    timeout: float = Field(default=-1, alias="dingtalk_timeout")
    """全局请求超时时间，值为正时生效"""

    def contains_any_keyword(self, text: str) -> bool:
        """
        检测字符串是否包含任意一个关键词，关键词切片为空也返回真

        Args:
            text (str): 待检测文本

        Returns:
            bool: 是否不添加关键词
        """
        if len(self.keywords) == 0:
            return True
        for keyword in self.keywords:
            if len(keyword) == 0:
                continue
            if keyword in text:
                return True
        return False

    async def send(self, message: Message, at: Optional[At] = None, uuid: Optional[str] = None, **kwargs):
        """
        自定义机器人发送群消息

        Args:
            message (Message): 要发送的消息
            at (Optional[At], optional): 被@的群成员信息
            uuid (Optional[str], optional): 消息幂等，发消息时接口调用超时或未知错误等报错，开发者可使用同一个消息幂等重试，避免重复发出消息
        """
        if len(self.secret) != 0:
            kwargs["timestamp"], kwargs["sign"] = generate_sign(self.secret)
        if self.timeout > 0:
            kwargs["timeout"] = self.timeout
        resp = await send(token=self.token, message=message, at=at, uuid=uuid, **kwargs)
        r = SendResponse.model_validate_json(resp.text)
        assert r.code == 0, r.msg

    async def text(self, content: str, at: Optional[At] = None, uuid: Optional[str] = None, **kwargs):
        """
        发送文本类型消息

        Args:
            content (str): 文本消息的内容
            at (Optional[At], optional): 被@的群成员信息
            uuid (Optional[str], optional): 消息幂等，发消息时接口调用超时或未知错误等报错，开发者可使用同一个消息幂等重试，避免重复发出消息
        """
        if not self.contains_any_keyword(content):
            content += self.keywords[0]
        await self.send(message=Text(content=content), at=at, uuid=uuid, **kwargs)

    async def link(
        self,
        title: str,
        text: str,
        message_url: str,
        pic_url: Optional[str] = None,
        at: Optional[At] = None,
        uuid: Optional[str] = None,
        **kwargs,
    ):
        """
        发送链接类型消息

        Args:
            title (str): 链接消息标题
            text (str): 链接消息的内容
            message_url (str): 点击消息跳转的链接
            pic_url (Optional[str], optional): 链接消息内的图片地址，建议使用上传媒体文件接口获取
            at (Optional[At], optional): 被@的群成员信息
            uuid (Optional[str], optional): 消息幂等，发消息时接口调用超时或未知错误等报错，开发者可使用同一个消息幂等重试，避免重复发出消息
        """
        if not self.contains_any_keyword(title) and not self.contains_any_keyword(text):
            text += self.keywords[0]
        await self.send(
            message=Link(
                title=title,
                text=text,
                messageUrl=message_url,
                picUrl=pic_url,
            ),
            at=at,
            uuid=uuid,
            **kwargs,
        )

    async def markdown(self, title: str, text: str, at: Optional[At] = None, uuid: Optional[str] = None, **kwargs):
        """
        发送 markdwon 类型消息

        Args:
            title (str): 消息会话列表中展示的标题，非消息体的标题
            text (str): markdown 类型消息的文本内容
            at (Optional[At], optional): 被@的群成员信息
            uuid (Optional[str], optional): 消息幂等，发消息时接口调用超时或未知错误等报错，开发者可使用同一个消息幂等重试，避免重复发出消息
        """
        if not self.contains_any_keyword(title) and not self.contains_any_keyword(text):
            text += self.keywords[0]
        await self.send(message=Markdown(title=title, text=text), at=at, uuid=uuid, **kwargs)

    async def action(
        self,
        title: str,
        text: str,
        single_title: Optional[str] = None,
        single_url: Optional[str] = None,
        at: Optional[At] = None,
        uuid: Optional[str] = None,
        **kwargs,
    ):
        """
        发送整体跳转 actionCard 类型消息

        Args:
            title (str): 消息会话列表中展示的标题，非消息体的标题
            text (str): actionCard 类型消息的正文内容，支持 markdown 语法
            single_title (Optional[str], optional): 按钮上显示的文本
            single_url (Optional[str], optional): 点击 singleTitle 按钮触发的链接
            at (Optional[At], optional): 被@的群成员信息
            uuid (Optional[str], optional): 消息幂等，发消息时接口调用超时或未知错误等报错，开发者可使用同一个消息幂等重试，避免重复发出消息
        """
        if not self.contains_any_keyword(title) and not self.contains_any_keyword(text):
            text += self.keywords[0]
        await self.send(
            message=ActionCard(
                title=title,
                text=text,
                singleTitle=single_title,
                singleURL=single_url,
            ),
            at=at,
            uuid=uuid,
            **kwargs,
        )

    async def actions(
        self,
        title: str,
        text: str,
        btns: Optional[List[ActionCardBtn]] = None,
        btn_orientation: Optional[str] = None,
        at: Optional[At] = None,
        uuid: Optional[str] = None,
        **kwargs,
    ):
        """
        发送独立跳转 actionCard 类型消息

        Args:
            title (str): 消息会话列表中展示的标题，非消息体的标题
            text (str): actionCard 类型消息的正文内容，支持 markdown 语法
            btns (Optional[List[ActionCardBtn]], optional): 按钮的信息列表
            btn_orientation (Optional[str], optional): 消息内按钮排列方式，0：按钮竖直排列，1：按钮横向排列
            at (Optional[At], optional): 被@的群成员信息
            uuid (Optional[str], optional): 消息幂等，发消息时接口调用超时或未知错误等报错，开发者可使用同一个消息幂等重试，避免重复发出消息
        """
        if not self.contains_any_keyword(title) and not self.contains_any_keyword(text):
            text += self.keywords[0]
        await self.send(
            message=ActionsCard(
                title=title,
                text=text,
                btns=btns,
                btnOrientation=btn_orientation,
            ),
            at=at,
            uuid=uuid,
            **kwargs,
        )

    async def feed(self, links: List[FeedCardLink], at: Optional[At] = None, uuid: Optional[str] = None, **kwargs):
        """
        发送 feedCard 类型消息

        Args:
            links (List[FeedCardLink]): feedCard 类型消息的内容列表
            at (Optional[At], optional): 被@的群成员信息
            uuid (Optional[str], optional): 消息幂等，发消息时接口调用超时或未知错误等报错，开发者可使用同一个消息幂等重试，避免重复发出消息
        """
        if len(self.keywords) != 0 and len(links) != 0:
            has_keyword = False
            for link in links:
                if self.contains_any_keyword(link.title):
                    has_keyword = True
                    break
            if not has_keyword:
                links[0].title += self.keywords[0]
        await self.send(message=FeedCard(links=links), at=at, uuid=uuid, **kwargs)

    async def error(self, message: LoguruMessage):
        """
        发送错误类型消息

        Args:
            message (LoguruMessage): 错误信息
        """
        record = dict(message.record)
        level: RecordLevel = record.get("level")
        exc_type, exc_value, _ = record.get("exception")
        time: datetime = record.get("time")

        header = "[" + level.name + "] " + record.get("message")
        content = f"{exc_type.__name__}: {exc_value}"
        footer = time.strftime("%Y-%m-%d %H:%M:%S")

        card = ErrorCard(
            title=ErrorLayout(
                header=" " + header + "\n",
                content=content + "\n",
                footer=footer,
            ),
            text=ErrorLayout(
                header="### " + header + "\n\n",
                content="".join("#### " + line for line in content.splitlines(True)) + "\n\n",
                footer="###### " + footer,
            ),
        )
        if not self.contains_any_keyword(str(card.title)) and not self.contains_any_keyword(str(card.text)):
            card.title.footer += self.keywords[0]
        await self.send(message=card)
