import base64
import hashlib
import hmac
import time
from typing import List, Optional, Tuple

import httpx
from pydantic import BaseModel, ConfigDict, Field

from .models import Message

session = httpx.AsyncClient()
URL = "https://oapi.dingtalk.com/robot/send"


class At(BaseModel):
    """
    被@的群成员信息
    """

    is_at_all: Optional[bool] = Field(None, alias="isAtAll")  # 是否@所有人
    at_mobiles: Optional[List[str]] = Field(None, alias="atMobiles")  # 被@的群成员手机号
    at_user_ids: Optional[List[str]] = Field(None, alias="atUserIds")  # 被@的群成员 userId

    model_config = ConfigDict(serialize_by_alias=True)


def generate_sign(secret: str) -> Tuple[int, str]:
    """
    生成加密时间戳和签名，加签的方式是将时间戳和密钥当做签名字符串，
    开发者服务内当前系统时间戳，单位是毫秒，与请求调用时间误差不能超过 1 小时，
    使用 HmacSHA256 算法计算签名，然后进行 Base64 编码，得到最终的签名

    Args:
        secret (str): 密钥

    Returns:
        Tuple[int, str]: 加密时间戳和签名
    """
    # 构造待签名字符串：毫秒级时间戳 + '\n' + 密钥
    timestamp = int(time.time() * 1000)
    message = f"{timestamp}\n{secret}".encode("utf-8")
    # 计算 HmacSHA256 签名
    key = secret.encode("utf-8")
    signature = hmac.new(key, message, hashlib.sha256).digest()
    signature_b64 = base64.b64encode(signature).decode("utf-8")
    return timestamp, signature_b64


async def send(
    token: str,
    message: Message,
    at: Optional[At] = None,
    uuid: Optional[str] = None,
    sign: Optional[str] = None,
    timestamp: Optional[int] = None,
    **kwargs,
):
    """
    自定义机器人发送群消息

    Args:
        token (str): 自定义机器人调用接口的凭证
        message (Message): 要发送的消息
        at (Optional[At], optional): 被@的群成员信息
        uuid (Optional[str], optional): 消息幂等，发消息时接口调用超时或未知错误等报错，开发者可使用同一个消息幂等重试，避免重复发出消息
        sign (Optional[str], optional): 使用时间戳和密钥生成的加密签名
        timestamp (Optional[int], optional): 开发者服务内当前系统时间戳，单位是毫秒，与请求调用时间误差不能超过 1 小时

    Returns:
        httpx.Response: 请求响应
    """
    params = {
        "access_token": token,
    }
    if sign is not None and timestamp is not None:
        params["sign"] = sign
        params["timestamp"] = timestamp

    body = {
        "msgtype": message.msg_type(),
        message.msg_type(): message.model_dump(),
    }
    if uuid is not None:
        body["msgUuid"] = uuid
    if at is not None:
        body["at"] = at.model_dump(exclude_none=True)

    return await session.post(URL, json=body, params=params, **kwargs)
