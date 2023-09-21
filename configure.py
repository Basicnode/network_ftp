# -*- coding: utf-8 -*-
# @Author: zt
# @Time: 2023/9/21 8:29
import configparser


class MyConfig:
    def __init__(self, filename):
        self.config = configparser.ConfigParser()
        self.config.read(filename)

    def get(self, section, key):
        return self.config.get(section, key)


config = MyConfig('config.ini')
# 测试验证
# value1 = config.get("section", 'port')
# value = config.get("section", 'file_save_path')
