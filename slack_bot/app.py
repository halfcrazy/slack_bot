# coding=utf-8
from flask import Flask

from flask_slackbot import SlackBot

import settings
import plugins
from ext import redis_store


plugin_modules = [
    getattr(plugins, plugin_name) for plugin_name in plugins.__all__
]


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)
    app.debug = True
    redis_store.init_app(app)
    return app

app = create_app()


def callback(kwargs):
    s = kwargs['text']
    if isinstance(s, unicode):
        s = s.encode('utf-8')
    data = {'message': s}
    bot = None
    for plugin_module in plugin_modules:
        if plugin_module.test(data, bot):
            rv = plugin_module.handle(data, bot, kv=None, app=app)
            return {'text': '!' + rv}

    return {'text': '!呵呵'}


def _filter(line):
    return line.startswith('!')


slackbot = SlackBot(app)
slackbot.set_handler(callback)
slackbot.filter_outgoing(_filter)

if __name__ == '__main__':
    app.run()
