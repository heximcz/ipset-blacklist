import yaml
from pathlib import PurePath
from src.Exceptions import ConfigException


class LoadConfig:
    """ Get config environment """

    def __init__(self):
        file_path = PurePath(__file__).parent.joinpath('../../config.yml')
        try:
            with open(file_path, 'r') as stream:
                try:
                    self.__config = yaml.load(stream, Loader=yaml.SafeLoader)
                    self.__check_ipset()
                except yaml.YAMLError:
                    raise ConfigException('Configuration Exception: Cannot load the config.yml file!')
        except IOError:
            raise ConfigException('Configuration Exception: IO error when the loading config.yml file..')

    def env(self, env):
        """
        Get one value by name from config file
        :param env:
        :return: string
        """
        return self.__config[env]

    def get_ipset(self):
        """
        Get ipset list
        :return: list
        """
        return self.__config['ipset']

    def __check_ipset(self):
        """ primitive check config file """
        ipset = self.get_ipset()
        if ipset is not None:
            for name in ipset:
                if ipset[name]['ipset-name'] is None:
                    raise ConfigException("Configuration Exception: the 'ipset-name' has no value in: " + name)
                if ipset[name]['list'] is None:
                    raise ConfigException("Configuration Exception: the 'list' has no value in: " + name)
        else:
            raise ConfigException("Configuration Exception: Config file has no values!")
