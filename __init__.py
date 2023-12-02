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
        if len(cfg['black_list']) != 1 and '12345' in cfg['black_list']:
            cfg['black_list'].remove('12345')
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
        if len(cfg['white_list']) != 1 and '12345' in cfg['white_list']:
            cfg['white_list'].remove('12345')
    config.config = cfg


def main():
    config = check_config()  # 检查配置项
    # 检查数据库
    from plugins.Gatekeeper.utils.database import DatabaseManager
    DatabaseManager().init_database()  # 初始化数据库

    # 导入黑白名单
    import_config(config)


main()

if __name__ == '__main__':
    main()
