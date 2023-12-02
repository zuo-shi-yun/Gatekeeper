"""实现黑白名单、临时用户逻辑"""
import copy
import datetime
import random

from plugins.Gatekeeper.utils.database import DatabaseManager


class HandleRequest:
    """处理请求"""

    def __init__(self, cfg: dict, **kwargs):
        self.qq = kwargs.get('launcher_id')
        self.sender_id = kwargs.get('sender_id')
        self.qq_type = 0 if kwargs.get('launcher_type') == 'person' else 1  # 0 个人 1 群

        self.e = None  # 异常
        self.ret_msg = ''  # 回复信息

        self.cfg = copy.deepcopy(cfg)

        self.status = self.handle()  # True放行False阻止

    # 判断处理请求状态
    def handle(self) -> bool:
        """判断处理请求状态"""
        if self.cfg['white_list_enable'] and self.is_in_white_list():
            return True  # 在白名单放行

        if self.cfg['black_list_enable'] and self.is_in_black_list():
            return False  # 在黑名单阻止

        if self.cfg['tourist_list_enable']:
            return self.is_tourist_out_usage()  # 返回临时用户是否超配额
        else:
            return True  # 没有开启临时用户放行

    # 判断是否在白名单
    def is_in_white_list(self) -> bool:
        """判断是否在白名单"""
        if self.qq in self.cfg.get('white_list'):
            return True
        else:
            return False

    # 判断是否在黑名单
    def is_in_black_list(self) -> bool:
        """判断是否在黑名单"""
        if self.qq in self.cfg.get('black_list'):
            return True
        else:
            return False

    # 判断临时用户是否超配额
    def is_tourist_out_usage(self) -> bool:
        svc = DatabaseManager()
        qq_list = svc.query(['qq'])  # 临时用户名单

        if self.qq in qq_list:  # 在临时用户数据库中
            use_time = svc.query(['time'], {'qq': self.qq})[0]  # 上次使用时间
            if self.is_last_use_time_out_refresh_time(self.cfg['tourist_refresh_days'], use_time):  # 若上次使用已过刷新时间范围
                current_time = datetime.datetime.now()
                formatted_time = current_time.strftime("%m-%d")

                if self.cfg['tourist_random_usage']:  # 开启了随机配额:
                    max_usage = random.randint(self.cfg['tourist_min_usage'], self.cfg['tourist_max_usage'])
                else:
                    max_usage = self.cfg['tourist_max_usage']
                # 更新数据库
                svc.update({'time': formatted_time, 'usage': 1, 'max_usage': max_usage}, {'qq': self.qq})
                return True
            else:  # 上次使用未过刷新时间范围
                use_time = svc.query(['usage'], {'qq': self.qq})[0]
                max_use_time = svc.query(['max_usage'], {'key': 'max_use_time'})[0]

                if use_time >= max_use_time:  # 已经超出则禁止使用
                    self.ret_msg = self.cfg['tourist_over_usage_msg'].format(self.cfg['tourist_refresh_days'])
                    return False
                else:  # 没有超出则允许使用并更新使用次数
                    svc.update({'use_cnt': use_time + 1}, {'qq': self.qq})
                    return True
        else:  # 没有在则插入并设次数为1
            if self.cfg['tourist_random_usage']:  # 开启了随机配额:
                max_usage = random.randint(self.cfg['tourist_min_usage'], self.cfg['tourist_max_usage'])
            else:
                max_usage = self.cfg['tourist_max_usage']
            # 插入数据库
            svc.insert(
                {'qq': self.qq, 'time': datetime.datetime.now().strftime("%m-%d"), 'use_cnt': 1,
                 'max_usage': max_usage})
            return True

    @staticmethod
    def is_last_use_time_out_refresh_time(timeout: int, time_last: str):
        today = datetime.date.today()

        time_last = datetime.datetime.strptime(time_last, "%m-%d").date()

        diff = time_last - today
        days_diff = diff.days

        return timeout <= days_diff
