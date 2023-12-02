"""
处理数据库操作。实现数据库CRUD逻辑
"""
import logging
import re
import sqlite3
import threading
import time
from sqlite3 import Cursor
from typing import List

from ruamel.yaml import YAML


# 数据库操作
class DatabaseManager:
    """数据库"""

    conn = None
    cursor = None

    def __init__(self, database_name: str = 'tourist'):
        self.reconnect()
        self.database = database_name

    # 连接到数据库文件
    def reconnect(self):
        """连接到数据库"""
        self.conn = sqlite3.connect('plugins/Gatekeeper/database.db', check_same_thread=False)
        # self.conn = sqlite3.connect('database.db', check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def __execute__(self, *args, **kwargs) -> Cursor:
        c = self.cursor.execute(*args, **kwargs)
        self.conn.commit()
        return c

    def insert(self, insert_data: dict) -> Cursor:
        """插入数据"""
        insert_key = '`' + '` ,`'.join(list(insert_data.keys())) + '`'
        # insert_value = ', '.join((f'"{v}"' if isinstance(v, str) else f'{v}') for v in insert_data.values())
        insert_value = ', '.join(['?' for _ in range(len(insert_data))])
        sql = f"insert into {self.database} ({insert_key}) values ({insert_value})"
        return self.__execute__(sql, tuple(insert_data.values()))

    def update(self, update_data: dict, where_data: dict) -> Cursor:
        """更新数据"""
        # update_data = [(f'`{k}`="{v}"' if isinstance(v, str) else f'`{k}`={v}') for k, v in update_data.items()]
        update_data_sql = [f'`{k}`=?' for k, v in update_data.items()]
        update_data_sql = ' ,'.join(update_data_sql)
        where_data_sql = [f'`{k}`=?' for k, v in where_data.items()]
        where_data_sql = ' and '.join(where_data_sql)
        sql = f"update {self.database} set {update_data_sql} where {where_data_sql}"
        return self.__execute__(sql, tuple(update_data.values()) + tuple(where_data.values()))

    def delete(self, where_delete: dict) -> Cursor:
        """删除数据"""
        where_delete_sql = [f'`{k}`=?' for k, v in where_delete.items()]
        where_delete_sql = ' and '.join(where_delete_sql)
        sql = f"delete from {self.database} where {where_delete_sql}"
        return self.__execute__(sql, tuple(where_delete.values()))

    def query(self, query_col: List[str], query_where: dict = None, reverse: bool = True) -> list:
        """查询数据.查询条件只实现了and关系"""
        # 构建查询列
        if len(query_col) == 1 and query_col[0] == '*':
            query_col_sql = '*'
        else:
            query_col_sql = '`' + '` ,`'.join(query_col) + '`'

        sql = f"select {query_col_sql} from {self.database}"

        # 构建查询条件
        if query_where:
            # 使用正则表达式代表模糊查询,正则的模式代表模糊查询模式
            query_where_sql = ' and '.join(
                [f'`{k}` like ?' if isinstance(v, re.Pattern)
                 else f'`{k}`=?'
                 for k, v in query_where.items()])
            sql += f" where {query_where_sql}"

        # 逆序
        if reverse:
            sql += ' order by id desc'

        if query_where:
            rows = self.__execute__(sql, tuple([v.pattern if isinstance(v, re.Pattern) else v
                                                for v in query_where.values()]))
        else:
            rows = self.__execute__(sql)

        res = []
        if len(query_col) == 1 and query_col[0] != '*':  # 只查询一行
            for row in rows:
                res.append(row[0])
        else:  # 查询多行
            for row in rows:  # 遍历行
                temp_res = {}
                for key in row.keys():  # 遍历列
                    temp_res[key] = row[key]  # 添加单元
                res.append(temp_res)

        return res

    # 初始化数据库
    def init_database(self):
        """
        初始化数据库
        :return:
        """

        self.__execute__("""
            create table if not exists tourist(
                `id` INTEGER primary key AUTOINCREMENT,  
                `qq` int,
                `usage` int,
                `max_usage` int,
                `time` text
            )
        """)

        logging.debug('数据库检测完毕')

    def close(self):
        self.conn.close()

    def __del__(self):
        self.close()


write_lock = threading.Lock()


# 配置文件操作
class ConfigManage:
    """配置文件操作"""

    def __init__(self):
        self.__config = self.get_config()

    # 获取配置文件
    @staticmethod
    def get_config() -> dict:
        """
        获取配置文件
        :return:
        """
        while write_lock.locked():  # 写时不能读
            time.sleep(0.1)
        with open('plugins/Gatekeeper/config.yml', 'r', encoding='utf-8') as f:
            yamls = YAML(typ='rt')
            config = yamls.load(f)
        return config

    # 重写配置文件
    @staticmethod
    def set_config(config):
        """
        设置配置文件
        :return:
        """
        with write_lock:  # 加锁
            with open('plugins/Gatekeeper/config.yml', 'w', encoding='utf-8') as f:
                yamls = YAML()
                yamls.dump(config, f)

    # 获得config
    @property
    def config(self):
        return self.__config

    # 设置config
    @config.setter
    def config(self, value: dict):
        self.__config = value
        self.set_config(self.__config)
