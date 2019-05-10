import sys
import os
import subprocess
from src.Parser import Parser
from src.Config import LoadConfig
from src.Exceptions import *


class IpSet:
    """ Create and Flush ipset """

    def __init__(self):
        self._parser = Parser()
        try:
            self._config = LoadConfig()
        except ConfigException as e:
            print(e)
            sys.exit(os.EX_UNAVAILABLE)

    def set_blacklist(self):
        """
        Create all ipsets from config file
        :return:
        """
        self.__process('blacklist-total', self._parser.create('blacklist-total'))
        self.__process('blacklist-port', self._parser.create('blacklist-port'))
        self.__process('whitelist', self._parser.create('whitelist'))

    def _create(self, name):
        """
        create ipset, if exist do nothing
        :param name
        :return:
        """
        command = [
            'ipset create -exist ' + name + ' hash:net family inet maxelem 536870912',
        ]
        self.__run(command)

    def _flush(self, name):
        """
        flush ipset
        :param name
        :return:
        """
        command = [
            'ipset flush ' + name,
        ]
        self.__run(command)

    def _add(self, name, ip):
        """
        add ip to ipset
        :param name
        :param ip
        :return:
        """
        command = [
            'ipset -exist add ' + name + ' ' + ip
        ]
        self.__run(command)

    def _swap(self, source, destination):
        """
        swap source ipset to destination ipset
        :param source:
        :param destination:
        :return:
        """
        command = [
            'ipset swap ' + destination + ' ' + source
        ]
        self.__run(command)

    def _destroy(self, name):
        """
        destroy ipset
        :param name:
        :return:
        """
        command = [
            'ipset destroy ' + name
        ]
        self.__run(command)

    @staticmethod
    def __run(command):
        """
        run subprocess command
        :param command:
        :return:
        """
        subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def __process(self, name, data):
        """
        :param name: of ipset
        :param data: parsed data
        :return:
        """
        env = self._config.env(name)
        # create temp ipset
        self._create(self._config.env('temp_ipset'))
        # flush tem ipset
        self._flush(self._config.env('temp_ipset'))
        # create ipset from 'name'
        self._create(env['ipset-name'])
        # append all ip to temp ipset, TODO: Is here any faster method?
        for ip in data:
            self._add(self._config.env('temp_ipset'), ip)
        # swap to original
        self._swap(self._config.env('temp_ipset'), env['ipset-name'])
        # destroy temp ipset
        self._destroy(self._config.env('temp_ipset'))
