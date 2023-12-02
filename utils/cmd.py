"""处理用户指令"""
from pkg.plugin.host import PluginHost

from utils.database import MyDict


class HandleCmd:
    """处理用户指令"""

    def __init__(self, cfg: MyDict, cmd: str, param: list, **kwargs):
        self.qq = kwargs.get('launcher_id')  # 发起者id,用户qq号或群qq号
        self.sender_id = kwargs.get('sender_id')  # 发送者id
        self.launcher_type = 0 if kwargs.get('launcher_type') == 'person' else 1  # 消息类型:0个人1群
        self.host = PluginHost()

        self.cmd = cmd  # 用户命令
        self.param = param  # 命令参数
        self.cfg = cfg  # 配置

        self.ret_msg = ''  # 回复信息
        self.e = None  # 异常

        self.had_handle_cmd = self.handle()  # 处理流程

    # 处理流程
    def handle(self) -> bool:
        """处理流程"""
        pass
