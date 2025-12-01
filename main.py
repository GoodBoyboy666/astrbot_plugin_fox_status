import asyncio
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

from .collector import get_all_info

@register("astrbot_plugin_fox_status", "GoodBoyboy", "一个用于获取 AstrBot 机器状态的插件。", "1.0.1")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
        
    @filter.command("状态",alias={'状态信息','status'})
    async def status(self, event: AstrMessageEvent):
        """获取状态"""
        event.stop_event()
        result = await asyncio.to_thread(get_all_info)
        yield event.plain_result(result)

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
