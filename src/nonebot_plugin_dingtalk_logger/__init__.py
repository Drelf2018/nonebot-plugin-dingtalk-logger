from typing import Any, Dict

from dingtalk import Bot
from nonebot import logger, get_driver
from loguru._handler import Message as LoguruMessage
from nonebot.plugin import PluginMetadata, get_plugin_config

from .config import Config

# 插件元数据，填写规范：https://nonebot.dev/docs/next/advanced/plugin-info#%E6%8F%92%E4%BB%B6%E5%85%83%E6%95%B0%E6%8D%AE
__plugin_meta__ = PluginMetadata(
    name="错误日志转发钉钉机器人",
    description="在使用 nonebot 自带的 logger 写入 ERROR 级别以上的日志时，会自动发送至钉钉机器人",
    usage="直接调用自带 logger 的方法",
    homepage="https://github.com/Drelf2018/nonebot-plugin-dingtalk-logger",
    type="library",
    config=Config,
    supported_adapters=None,  # 适配器支持集合
)

driver = get_driver()
plugin_config = get_plugin_config(Config)
ding = Bot(
    token=plugin_config.dingtalk_token,
    secret=plugin_config.dingtalk_secret,
    keywords=plugin_config.dingtalk_keywords,
    timeout=plugin_config.dingtalk_timeout,
)


async def handler(message: LoguruMessage):
    """
    日志处理器

    Args:
        message (LoguruMessage): 错误日志信息
    """
    extra: Dict[str, Any] = dict(message.record).get("extra", {})
    if not extra.get("dingtalk_handler", False):
        try:
            await ding.error(message=message)
        except:
            logger.bind(dingtalk_handler=True).exception("转发出错")


@driver.on_startup
async def add_logger_handler():
    """
    添加日志处理器
    """
    logger.add(handler, level=plugin_config.dingtalk_level)  # type: ignore
