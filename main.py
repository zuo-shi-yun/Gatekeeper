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
        check_plugin()  # 检查插件完整性

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


# 检查配置文件
def check_config():
    """检查配置文件"""
    from plugins.Gatekeeper.utils.database import ConfigManage

    cfg = ConfigManage()
    config = cfg.get_config()

    if 'normal_cmd' not in config:
        raise ValueError('缺少normal_cmd配置')
    elif not isinstance(config['normal_cmd'], bool):
        raise ValueError('normal_cmd配置项错误')

    if 'prevent_postorder' not in config:
        raise ValueError('缺少prevent_postorder配置')
    elif not isinstance(config['prevent_postorder'], bool):
        raise ValueError('prevent_postorder配置项错误')

    if 'black_list_enable' not in config:
        raise ValueError('缺少black_list_enable配置')
    elif not isinstance(config['black_list_enable'], bool):
        raise ValueError('black_list_enable配置项错误')

    if 'white_list_enable' not in config:
        raise ValueError('缺少white_list_enable配置')
    elif not isinstance(config['white_list_enable'], bool):
        raise ValueError('white_list_enable配置项错误')

    if 'tourist_list_enable' not in config:
        raise ValueError('缺少tourist_list_enable配置')
    elif not isinstance(config['tourist_list_enable'], bool):
        raise ValueError('tourist_list_enable配置项错误')

    if 'tourist_random_usage' not in config:
        raise ValueError('缺少tourist_random_usage配置')
    elif not isinstance(config['tourist_random_usage'], bool):
        raise ValueError('tourist_random_usage配置项错误')

    if 'tourist_max_usage' not in config:
        raise ValueError('缺少tourist_max_usage配置')
    elif not isinstance(config['tourist_max_usage'], int) or config['tourist_max_usage'] < 0:
        raise ValueError('tourist_max_usage配置项错误')

    if 'tourist_refresh_days' not in config:
        raise ValueError('缺少tourist_refresh_days配置')
    elif not isinstance(config['tourist_refresh_days'], int) or config['tourist_refresh_days'] < 0:
        raise ValueError('tourist_refresh_days配置项错误')

    if 'tourist_min_usage' not in config:
        raise ValueError('缺少tourist_min_usage配置')
    elif not isinstance(config['tourist_min_usage'], int) \
            or config['tourist_min_usage'] > config['tourist_max_usage'] \
            or config['tourist_min_usage'] < 0:
        raise ValueError('tourist_min_usage配置项错误')

    if 'white_list' not in config:
        raise ValueError('缺少white_list配置')
    elif not isinstance(list(config['white_list']), list) or not all(
            isinstance(elem, int) for elem in config['white_list']):
        raise ValueError('white_list配置项错误')

    if 'black_list' not in config:
        raise ValueError('缺少black_list配置')
    elif not isinstance(list(config['black_list']), list) or not all(
            isinstance(elem, int) for elem in config['black_list']):
        raise ValueError('black_list配置项错误')

    if 'tourist_over_usage_msg' not in config:
        raise ValueError('缺少tourist_over_usage_msg配置')
    elif not isinstance(config['tourist_over_usage_msg'], str):
        raise ValueError('tourist_over_usage_msg配置项错误')
    return cfg


# 导入黑白名单
def import_config(config):
    """导入黑白名单"""
    cfg = config.get_config()
    # 黑名单
    import banlist
    ban_person = banlist.person
    ban_group = banlist.group
    if len(cfg['black_list']) == 1 and cfg['black_list'][0] is None:  # 为空则添加管理员
        cfg['black_list'] = ban_person + ban_group
    else:  # 不为空则追加管理员
        for i in ban_person + ban_group:
            if i not in cfg['black_list']:
                cfg['black_list'].append(i)
        # 删除示例qq
        if len(cfg['black_list']) != 1 and 12345 in cfg['black_list']:
            cfg['black_list'].remove(12345)
    # 白名单
    from pkg.utils import context
    admin_qq = getattr(context.get_config(), 'admin_qq')  # 管理员qq
    if not isinstance(admin_qq, list):
        admin_qq = [admin_qq]

    if len(cfg['white_list']) == 1 and cfg['white_list'][0] is None:  # 为空则添加管理员
        cfg['white_list'] = admin_qq
    else:  # 不为空则追加管理员
        for i in admin_qq:
            if i not in cfg['white_list']:
                cfg['white_list'].append(i)
        # 删除示例qq
        if len(cfg['white_list']) != 1 and 12345 in cfg['white_list']:
            cfg['white_list'].remove(12345)
    config.config = cfg


def check_plugin():
    config = check_config()  # 检查配置项
    # 检查数据库
    from plugins.Gatekeeper.utils.database import DatabaseManager
    DatabaseManager().init_database()  # 初始化数据库

    # 导入黑白名单
    import_config(config)


if __name__ == 'main':
    pass
