# my_config.py
import configparser
# 创建configparser对象
config = configparser.ConfigParser()
# 读取INI文件
config.read('config.ini')
# 获取配置值
debug = config.getboolean('DEFAULT', 'debug')
port = config.getint('DEFAULT', 'port')
host = config.get('DEFAULT', 'host')
secretId = config.get('DEFAULT', 'secretId')
secretKey = config.get('DEFAULT', 'secretKey')