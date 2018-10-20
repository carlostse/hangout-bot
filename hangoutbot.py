#  hangout-bot
#
#  Copyright © 2018 Carlos Tse <carlos@aboutmy.info>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from argparse import ArgumentParser
from os import environ, path

from aiotg import Bot
from yaml import load as yaml_load

from plugins import PluginManager


class HangoutBot(object):

    def __init__(self, args):
        self.env: str = args.env or environ.get('env', 'test')
        self.debug: bool = args.v or bool(environ.get('debug'))

    def run(self):
        with open(path.join('config', self.env + '.yaml')) as cfg_file:
            cfg = yaml_load(cfg_file)

        bot = Bot(cfg['token'])
        PluginManager.load(bot, cfg)
        bot.run(debug=self.debug, reload=False)


if __name__ == '__main__':
    parser = ArgumentParser(description='Hangout Bot')
    parser.add_argument('env', help='enviroment, it will the config in config/<env>.yaml')
    parser.add_argument('-v', action='store_true', help='verbose debug mode')
    HangoutBot(parser.parse_args()).run()
