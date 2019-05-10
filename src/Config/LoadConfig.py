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
                    self.__config = yaml.load(stream)
                except yaml.YAMLError:
                    raise ConfigException('Exception: load_config_yaml_error')
        except IOError:
            raise ConfigException('Exception: load_config_io_error')

    def env(self, env):
        """
        Get one value by name from config file
        :param env:
        :return:
        """
        return self.__config[env]
