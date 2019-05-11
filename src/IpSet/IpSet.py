import subprocess
from src.Parser import Parser
from src.Config import LoadConfig


class IpSet:
    """ Create and Flush ipset """

    def __init__(self, config: LoadConfig):
        """
        :param config: instanceof LoadConfig
        """
        self.__parser = Parser(config)
        self.__config = config
        self.__ipset = self.__config.get_ipset()
        self.verbose = self.__config.env('verbose')

    def set_blacklist(self):
        """
        Dynamically create all ipsets from the config file
        :return:
        """

        for name in self.__ipset:
            if self.verbose:
                print("Start create: " + self.__ipset[name]['ipset-name'])

            # create ipset
            self.__process(name, self.__parser.create(name))

            if self.verbose:
                print('Done')

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
        env = self.__ipset[name]
        # create temp ipset
        self._create(self.__config.env('ipset-temp'))
        # flush tem ipset
        self._flush(self.__config.env('ipset-temp'))
        # create ipset from 'name'
        self._create(env['ipset-name'])
        # append all ip to temp ipset, TODO: Is here any faster method?
        for ip in data:
            self._add(self.__config.env('ipset-temp'), ip)
        # swap to original
        self._swap(self.__config.env('ipset-temp'), env['ipset-name'])
        # destroy temp ipset
        self._destroy(self.__config.env('ipset-temp'))
