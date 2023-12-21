"""处理用户指令"""
import base64
import copy

from mirai import Image

from pkg.plugin.host import PluginHost
from plugins.Gatekeeper.utils.HostConfig import HostConfig
from plugins.Gatekeeper.utils.database import ConfigManage
from plugins.Gatekeeper.utils.md.data_source import md_to_pic


class HandleCmd:
    """处理用户指令"""

    def __init__(self, cfg: dict, cmd: str, param: list, **kwargs):
        self.qq = kwargs.get('launcher_id')  # 发起者id,用户qq号或群qq号
        self.sender_id = kwargs.get('sender_id')  # 发送者id
        self.launcher_type = 0 if kwargs.get('launcher_type') == 'person' else 1  # 消息类型:0个人1群
        self.host = PluginHost()

        self.cmd = cmd  # 用户命令
        self.param = param  # 命令参数
        self.__cfg = ConfigManage.get_config()  # 配置

        self.ret_msg = ''  # 回复信息
        self.e = None  # 异常

        self.had_handle_cmd = self.handle()  # 处理流程

    # 处理流程
    def handle(self) -> bool:
        """处理流程"""
        handle_func = {
            '添加白名单': self.add_white_list,
            '添加黑名单': self.add_black_list,
            '删除白名单': self.remove_white_list,
            '删除黑名单': self.remove_black_list,
            '查询白名单': self.get_white_list,
            '查询黑名单': self.get_black_list,
            '打开白名单': self.open_white_list,
            '打开黑名单': self.open_black_list,
            '关闭白名单': self.close_white_list,
            '关闭黑名单': self.close_black_list,
            '打开临时用户': self.open_tourist,
            '关闭临时用户': self.close_tourist,
            '打开随机配额': self.open_random_usage,
            '关闭随机配额': self.close_random_usage,
            '设置最高': self.set_tourist_max_usage,
            '设置最低': self.set_tourist_min_usage,
            '设置天数': self.set_tourist_refresh_day,
            '设置信息': self.set_out_usage_info,
            '查询配置': self.get_all_cfg,
            '打开普通指令': self.open_normal_cmd,
            '关闭普通指令': self.close_normal_cmd,
            '打开插件阻止': self.open_prevent_order,
            '关闭插件阻止': self.close_prevent_order,
            '看门狗': self.help,
        }

        admin_qq = HostConfig.get('admin_qq')
        if not isinstance(admin_qq, list):
            admin_qq = [admin_qq]

        if self.cmd in handle_func and self.sender_id in admin_qq:  # 是本插件处理指令且是管理员
            handle_func[self.cmd]()
            return True
        else:
            return False

    # 异常包裹
    @staticmethod
    def decorator(func):
        def wrapper(self, *args, **kwargs):  # self is the instance of class A
            try:
                ret = func(self, *args, **kwargs)
                self.ret_msg = self.ret_msg or '成功'
                self.cfg = ConfigManage.get_config()
                return ret
            except Exception as e:
                self.ret_msg = f'失败!{e}'
                self.e = e

        return wrapper

    # 添加白名单
    @decorator
    def add_white_list(self):
        """添加白名单"""
        config = self.cfg

        for i in self.param:
            if int(i) not in config['white_list']:
                config['white_list'].append(int(i))

        ConfigManage.set_config(config)

    # 添加黑名单
    @decorator
    def add_black_list(self):
        """添加黑名单"""
        config = self.cfg

        for i in self.param:
            if int(i) not in config['black_list']:
                config['black_list'].append(int(i))

        ConfigManage.set_config(config)

    # 删除白名单
    @decorator
    def remove_white_list(self):
        """删除白名单"""
        config = self.cfg

        for i in self.param:
            if int(i) in config['white_list']:
                config['white_list'].remove(int(i))

        ConfigManage.set_config(config)

    # 删除黑名单
    @decorator
    def remove_black_list(self):
        """删除黑名单"""
        config = self.cfg

        for i in self.param:
            if int(i) in config['black_list']:
                config['black_list'].remove(int(i))

        ConfigManage.set_config(config)

    # 得到白名单
    @decorator
    def get_white_list(self):
        # 得到白名单
        res = [f"{i + 1}.{self.cfg['white_list'][i]}" for i in range(len(self.cfg['white_list']))]
        self.ret_msg = '\n'.join(res)

    # 得到黑名单
    @decorator
    def get_black_list(self):
        # 得到黑名单
        res = [f"{i + 1}.{self.cfg['black_list'][i]}" for i in range(len(self.cfg['black_list']))]
        self.ret_msg = '\n'.join(res)

    # 开启白名单
    @decorator
    def open_white_list(self):
        """开启白名单"""
        cfg = self.cfg
        cfg['white_list_enable'] = True

        ConfigManage.set_config(cfg)

    # 开启黑名单
    @decorator
    def open_black_list(self):
        """开启黑名单"""
        cfg = self.cfg
        cfg['black_list_enable'] = True

        ConfigManage.set_config(cfg)

    # 关闭白名单
    @decorator
    def close_white_list(self):
        cfg = self.cfg
        cfg['white_list_enable'] = False

        ConfigManage.set_config(cfg)

    # 关闭黑名单
    @decorator
    def close_black_list(self):
        """关闭黑名单"""
        cfg = self.cfg
        cfg['black_list_enable'] = True

        ConfigManage.set_config(cfg)

    # 打开临时用户
    @decorator
    def open_tourist(self):
        """打开临时用户"""
        cfg = self.cfg
        cfg['tourist_list_enable'] = True

        ConfigManage.set_config(cfg)

    # 关闭临时用户
    @decorator
    def close_tourist(self):
        """关闭临时用户"""
        cfg = self.cfg
        cfg['tourist_list_enable'] = False

        ConfigManage.set_config(cfg)

    # 打开随即配额
    @decorator
    def open_random_usage(self):
        """打开随即配额"""
        cfg = self.cfg
        cfg['tourist_random_usage'] = True

        ConfigManage.set_config(cfg)

    # 关闭随即配额
    @decorator
    def close_random_usage(self):
        """关闭随即配额"""
        cfg = self.cfg
        cfg['tourist_random_usage'] = False

        ConfigManage.set_config(cfg)

    # 设置配额最大值
    @decorator
    def set_tourist_max_usage(self):
        """设置配额最大值"""
        cfg = self.cfg
        cfg['tourist_max_usage'] = int(self.param[0])

        ConfigManage.set_config(cfg)

    # 设置配额最小值
    @decorator
    def set_tourist_min_usage(self):
        """设置配额最小值"""
        cfg = self.cfg
        cfg['tourist_min_usage'] = int(self.param[0])

        ConfigManage.set_config(cfg)

    # 设置配额刷新天数
    @decorator
    def set_tourist_refresh_day(self):
        """设置随即配额刷新天数"""
        cfg = self.cfg
        cfg['tourist_refresh_days'] = int(self.param[0])

        ConfigManage.set_config(cfg)

    # 设置配额超限提示信息
    @decorator
    def set_out_usage_info(self):
        """设置配额超限提示信息"""
        cfg = self.cfg
        cfg['tourist_over_usage_msg'] = '\n'.join(self.param)
        ConfigManage.set_config(cfg)

    # 得到全部配置
    @decorator
    def get_all_cfg(self):
        """得到全部配置"""
        cfg = self.cfg

        self.ret_msg = '\n'.join([f'{k}:{v}' for k, v in cfg.items()])

    # 打开普通指令
    @decorator
    def open_normal_cmd(self):
        """打开普通指令"""
        cfg = self.cfg
        cfg['normal_cmd'] = True
        ConfigManage.set_config(cfg)

    # 关闭普通指令
    @decorator
    def close_normal_cmd(self):
        """关闭普通指令"""
        cfg = self.cfg
        cfg['normal_cmd'] = False
        ConfigManage.set_config(cfg)

    # 打开阻止插件传递
    @decorator
    def open_prevent_order(self):
        """打开阻止插件传递"""
        cfg = self.cfg
        cfg['prevent_postorder'] = True

        ConfigManage.set_config(cfg)

    # 关闭阻止插件传递
    @decorator
    def close_prevent_order(self):
        """打开阻止插件传递"""
        cfg = self.cfg
        cfg['prevent_postorder'] = False

        ConfigManage.set_config(cfg)

    # 获得config
    @property
    def cfg(self):
        return copy.deepcopy(self.__cfg)

    # 设置config
    @cfg.setter
    def cfg(self, value: dict):
        self.__cfg = value

    # 帮助
    @decorator
    def help(self):
        """帮助"""
        md_image = md_to_pic(md_path=r'plugins\Gatekeeper\HELP.md', width=800)
        b64_img = base64.b64encode(md_image).decode()
        self.ret_msg = Image(base64=b64_img, width=1050, height=5000)
