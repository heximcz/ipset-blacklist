# import subprocess
from src.Parser import Parser
from src.Config import LoadConfig


class IpSetFile:
    """ Create and Flush ipset """

    def __init__(self, config: LoadConfig):
        """
        :param config: instanceof LoadConfig
        """
        self.__parser = Parser(config)
        self.__config = config
        self.__ipset = self.__config.get_ipset()
        self.verbose = self.__config.env('verbose')

    def create_file(self):
        """
        Dynamically create all ipsets from the config file
        :return:
        """

        for name in self.__ipset:
            if self.verbose:
                print("Start create: " + self.__ipset[name]['ipset-name'])

            filename = self.__config.env('folder') + name + '.sh'
            file = open(filename, "w")
            file.write("#!/bin/bash\n")
            for ip in self.__parser.create(name):
                if name != 'whitelist-total':
                    file.write('ipset -exist add ' + self.__ipset[name]['ipset-name'] + ' ' + ip + '\n')
                else:
                    file.write('ipset -exist del ' + self.__ipset[name]['ipset-name'] + ' ' + ip + '\n')
            file.close()

        if self.verbose:
            print('Done')
