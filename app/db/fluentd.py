
from fluent import sender

from app.utils import const

class Fluentd:
    __logger = None

    def __init__(self):
        self.__logger = sender.FluentSender(const.fluentd.label,
            host=const.fluentd.host,
            port=const.fluentd.port
        )

    def log(self, data):
        self.__logger.emit('web', data)
