from nonebot import get_driver, get_plugin_config, logger
from nonebot.plugin import PluginMetadata

from .dingtalk import Bot

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-dingtalk-logger",
    description="在使用 nonebot 自带的 logger 写入 ERROR 级别以上的日志时，会自动发送至钉钉机器人",
    usage="直接调用 logger 的方法",
    type="library",
    config=Bot,
)

driver = get_driver()
plugin_config = get_plugin_config(Bot)


@driver.on_startup
async def add_logger_handler():
    """
    添加日志处理器
    """
    logger.add(plugin_config.error, level="ERROR")
