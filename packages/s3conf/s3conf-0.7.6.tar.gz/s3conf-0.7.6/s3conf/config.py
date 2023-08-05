import os
import logging
from configparser import ConfigParser

from .files import File


logger = logging.getLogger(__name__)


def _lookup_config_folder(initial_folder='.'):
    if not initial_folder:
        config_folder = os.path.join('.', '.s3conf')
        logger.debug('Config folder detected: %s', config_folder)
        return config_folder
    current_path = os.path.abspath(initial_folder)
    path_items = set(os.listdir(current_path))
    if '.s3conf' in path_items:
        s3conf_folder = os.path.join(current_path, '.s3conf')
        if os.path.isdir(s3conf_folder):
            config_folder = os.path.join(current_path, '.s3conf')
            logger.debug('Config folder detected: %s', config_folder)
            return config_folder
    return _lookup_config_folder(os.path.dirname(current_path) if current_path != '/' else None)


LOCAL_CONFIG_FOLDER = _lookup_config_folder()
LOCAL_CONFIG_FILE = os.path.join(LOCAL_CONFIG_FOLDER, 'config')


class EnvironmentResolver:
    def get(self, item, default=None):
        return os.environ.get(item, default)


class ConfigFileResolver:
    def __init__(self, config_file, section=None):
        self.config_file = os.path.expanduser(config_file)
        self.section = section or 'DEFAULT'
        self._config = None

    @property
    def config(self):
        if not self._config:
            self._config = ConfigParser()
            self._config.read(self.config_file)
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    def get(self, item, default=None, section=None):
        return self.config.get(section or self.section, item, fallback=default)

    def edit(self, create=False):
        File(self.config_file).edit(create=create)

    def sections(self):
        return self.config.sections()


class Settings:
    def __init__(self, section=None, config_file=None):
        config_file = config_file or LOCAL_CONFIG_FILE
        if section:
            self.resolvers = [
                ConfigFileResolver(config_file, section),
                EnvironmentResolver(),
            ]
        else:
            self.resolvers = [
                EnvironmentResolver(),
                ConfigFileResolver(config_file, section),
            ]

    def __getitem__(self, item):
        for resolver in self.resolvers:
            value = resolver.get(item)
            if value:
                break
        else:
            logger.debug('Entry %s not found', item)
            raise KeyError()
        logger.debug('Entry %s has value %s', item, value)
        return value

    def get(self, item, default=None):
        try:
            return self[item]
        except KeyError:
            logger.debug('Key %s not found, returning default %s', item, default)
            return default
