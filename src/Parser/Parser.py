import re
import urllib3
from src.Config import LoadConfig
from src.Exceptions import *


class Parser:
    """ Parse URLs input """

    def __init__(self, config: LoadConfig):
        timeout = urllib3.Timeout(connect=5.0, read=7.0)
        self.__http = urllib3.PoolManager(timeout=timeout)
        self.__config = config

    def create(self, name):
        """
        Create data from URLs
        :param name:
        :return:
        """
        ipset = self.__config.get_ipset()
        data = []
        # get url(s) list:
        if ipset[name]['list'] is not None:
            for val in ipset[name]['list']:
                try:
                    http_data = self.__load(val)
                    data = data + self.__extract_ips(http_data)
                except BlacklistException:
                    pass
        # get local file(s):
        if ipset[name]['file'] is not None:
            for val in ipset[name]['file']:
                content = self.__get_files(val)
                if content is not None:
                    data = data + self.__extract_ips(content)
        return data

    def __load(self, url):
        """ load data from url """
        r = self.__http.request('GET', url)
        if r.status != 200:
            raise BlacklistException
        return r.data.decode('utf-8')

    @staticmethod
    def __get_files(path):
        try:
            with open(path, 'r') as f:
                content = f.read()
        except IOError:
            print('IO error while open file: ' + path)
            return None
        return content

    @staticmethod
    def __extract_ips(content):
        ip_pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2}|)')
        ip = re.findall(ip_pattern, content)
        return ip

