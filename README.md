<div align="center">

# nonebot-plugin-dingtalk-logger

_✨ 将错误日志推送至钉钉机器人的 NoneBot 插件 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/Drelf2018/nonebot-plugin-dingtalk-logger.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-dingtalk-logger">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-dingtalk-logger.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>

## 📖 介绍

在使用 `nonebot` 自带的 `logger` 写入 `ERROR` 级别以上的日志时，会自动发送至钉钉机器人

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-dingtalk-logger

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-dingtalk-logger
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-dingtalk-logger
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-dingtalk-logger
</details>


打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_dingtalk_logger"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| DINGTALK_TOKEN | 是 | 无 | 调用接口的凭证，钉钉提供的 `Webhook` 链接中 `access_token` 的值 |
| DINGTALK_SECRET | 否 | `""` | 安全密钥，安全设置项选择了加签后，提供的 `SEC` 开头的字符串 |
| DINGTALK_KEYWORDS | 否 | `[]` | 自定义关键词，创建机器人时在安全设置项填入的所有关键词 |
| DINGTALK_TIMEOUT | 否 | `None` | 请求超时时间 |
| DINGTALK_LEVEL | 否 | `"ERROR"` | 日志转发等级 |
