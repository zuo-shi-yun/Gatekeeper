from pkg.plugin.host import EventContext, PluginHost
from pkg.plugin.models import *
from plugins.GateKeeper.utils.cmd import HandleCmd
from plugins.GateKeeper.utils.database import ConfigManage

"""
黑白名单、临时用户机制
"""


# 注册插件
@register(name="Gatekeeper", description="黑白名单、临时用户机制", version="1.0", author="zuoShiYun")
class DiscountAssistant(Plugin):
    def __init__(self, plugin_host: PluginHost):
        self.host = plugin_host
        self.cfg = ConfigManage.get_config()

    # 处理群、个人指令-!cmd形式
    @on(PersonCommandSent)
    @on(GroupCommandSent)
    def handle_cmd(self, event: EventContext, **kwargs):
        handle = HandleCmd(self.cfg, kwargs['command'], kwargs['params'], **kwargs)

        # 判断是否是本插件处理指令
        if handle.had_handle_cmd:
            event.prevent_default()
            event.is_prevented_postorder()

            if handle.ret_msg:  # 发送回复信息
                event.add_return("reply", [handle.ret_msg])

            if handle.e:  # 显式报错
                raise handle.e

    # 处理群、个人指令-非!cmd形式
    @on(PersonNormalMessageReceived)
    @on(GroupNormalMessageReceived)
    def handle_normal_cmd(self, event: EventContext, **kwargs):
        if self.cfg['normal_cmd']:  # 已开启非!cmd形式的命令
            text = kwargs['text_message'].split()  # 信息文本
            handle = HandleCmd(self.cfg, text[0], text[1::], **kwargs)

            # 判断是否是本插件处理指令
            if handle.had_handle_cmd:
                event.prevent_default()
                event.is_prevented_postorder()

                if handle.ret_msg:  # 发送回复信息
                    event.add_return("reply", [handle.ret_msg])

                if handle.e:  # 显式报错
                    raise handle.e

    # 插件卸载时触发
    def __del__(self):
        pass


if __name__ == 'main':
    pass
