"""实现黑白名单、临时用户逻辑"""


class HandleRequest:
    """处理请求"""

    def __init__(self, **kwargs):
        self.qq = kwargs.get('launcher_id')
        self.sender_id = kwargs.get('sender_id')
        self.qq_type = 0 if kwargs.get('launcher_type') == 'person' else 1  # 0 个人 1 群

        self.e = None  # 异常

        self.status = self.handle()  # True放行False阻止

    # 判断处理请求状态
    def handle(self) -> bool:
        """判断处理请求状态"""
        pass
