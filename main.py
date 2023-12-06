from pkg.plugin.host import EventContext, PluginHost
from pkg.plugin.models import *
from plugins.Gatekeeper.utils.Filter import HandleRequest
from plugins.Gatekeeper.utils.cmd import HandleCmd
from plugins.Gatekeeper.utils.database import ConfigManage

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
            event.prevent_postorder()

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

            # 过滤器
            handle_request = HandleRequest(self.cfg, **kwargs)
            if not handle_request.status:  # 禁止请求
                event.add_return('reply', [handle_request.ret_msg])
                event.prevent_default()

                if self.cfg['prevent_postorder']:  # 是否阻止其他插件
                    event.prevent_postorder()
            # 显式报错
            if handle_request.e:
                raise handle_request.e

            # 处理指令
            handle_cmd = HandleCmd(self.cfg, text[0], text[1::], **kwargs)

            # 判断是否是本插件处理指令
            if handle_cmd.had_handle_cmd:
                event.prevent_default()
                event.prevent_postorder()

                if handle_cmd.ret_msg:  # 发送回复信息
                    event.add_return("reply", [handle_cmd.ret_msg])
                # 显式报错
                if handle_cmd.e:
                    raise handle_cmd.e

    # 插件卸载时触发
    def __del__(self):
        pass


if __name__ == 'main':
    pass
