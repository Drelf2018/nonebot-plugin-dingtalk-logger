from typing import List, Optional

from pydantic import Field, BaseModel


class Config(BaseModel):
    """钉钉机器人配置"""

    dingtalk_token: str
    """调用接口的凭证，钉钉提供的 Webhook 链接中 access_token 的值"""

    dingtalk_secret: str = ""
    """安全密钥，创建机器人时在安全设置项选择了加签后，钉钉提供的 SEC 开头的字符串"""

    dingtalk_keywords: List[str] = Field(default_factory=list)
    """自定义关键词，创建机器人时在安全设置项填入的所有关键词"""

    dingtalk_timeout: Optional[float] = None
    """请求超时时间"""

    dingtalk_level: str = "ERROR"
    """日志转发等级"""
