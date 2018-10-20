from abc import abstractmethod
from importlib import import_module
from inspect import getmembers, isclass
from os import path, listdir
from re import match

from aiotg.bot import Bot, Chat


class Intent(object):
    """Base class for plugins.

    """
    def __init__(self, config):
        self._cfg = config

    @property
    @abstractmethod
    def command(self) -> str:
        """Return the regexp for the comman.

        :return: regexp
        :rtype: str
        """
        pass

    @abstractmethod
    async def execute(self, chat: Chat, rematch: match):
        """Execute the plugin to reply user.

        :param chat: chat
        :type chat: aiotg.bot.Chat
        :param rematch: regex match
        :type rematch: re.match
        """
        pass


class PluginManager(object):
    """Plugs manager.

    """
    def __init__(self):
        self.dirname = None
        self.plugins = dict()

    @staticmethod
    def load(bot: Bot, config: dict, directory: str=path.dirname(path.abspath(__file__))):
        """Load the plugins and return the bot.

        :param bot: bot
        :type bot: aiotg.bot.Bot
        :param config: user config
        :type config: dict
        :param directory: plugins directory
        :type directory: str
        :return: bot
        :rtype: aiotg.bot.Bot
        """
        mgr = PluginManager()
        mgr.load_directory(directory)
        for _, obj in mgr.plugins.items():
            plugin = obj(config)
            bot.add_command(plugin.command, plugin.execute)
        return bot

    def load_file(self, filepath: str):
        """Load the plugin file.

        :param filepath: file path
        :type filepath: str
        """
        _, filename = path.split(filepath)
        _, dirname = path.split(self.dirname)
        module = import_module(dirname + '.' + path.splitext(filename)[0])

        for name, obj in getmembers(module):
            if self.filter(name, obj):
                self.plugins[name] = obj

    def load_directory(self, directory: str, recursive: bool=False):
        """Load the plugins in directory.

        :param directory: directory path
        :type directory: str
        :param recursive: recursive
        :type recursive: bool
        """
        self.dirname = directory

        for filename in listdir(directory):
            filepath = path.join(directory, filename)

            if path.isfile(filepath):
                self.load_file(filepath)
                continue

            if path.isdir(filepath) and recursive:
                self.load_directory(filepath, recursive)

        print('found %d plugins' % len(self.plugins))
        print('loaded plugins: %s' % ', '.join(self.plugins.keys()))

    @staticmethod
    def filter(name: str, obj: type) -> bool:
        """Filter the plugin.

        :param name: name of the object
        :type name: str
        :param obj: type
        :type obj: object
        :return: True if the plugin should be loaded
        :rtype: bool
        """
        return not name.startswith('__') and isclass(obj) and issubclass(obj, Intent) and obj is not Intent
