import os
import sys
import re
import urllib3
from src.Config import LoadConfig
from src.Exceptions import *


class Parser:
    """ Parse URLs input """

    def __init__(self):
        timeout = urllib3.Timeout(connect=5.0, read=7.0)
        self.__http = urllib3.PoolManager(timeout=timeout)
        try:
            self.__config = LoadConfig()
        except ConfigException as e:
            print(e)
            sys.exit(os.EX_UNAVAILABLE)

    def create(self, name):
        """
        Create data from URLs
        :param name:
        :return:
        """
        env = self.__config.env(name)
        data = []
        for val in env['list']:
            try:
                http_data = self.__load(val)
                data = data + self.__extract_ips(http_data)
            except BlacklistException:
                pass
        return data

    def __load(self, url):
        """ load data from url """
        r = self.__http.request('GET', url)
        if r.status != 200:
            raise BlacklistException
        return r.data.decode('utf-8')

    @staticmethod
    def __extract_ips(content):
        ip_pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2}|)')
        ip = re.findall(ip_pattern, content)
        return ip
