import logging
import traceback
import datetime

from app.db import fluentd

from app.utils import session, reference

class Logger:
    __logger = None
    __fluentd = None

    def __init__(self, module):
        self.__module = module
        self.__logger = logging.getLogger(module)
        self.__logger.setLevel(logging.DEBUG)

        # create console handler
        fmt = logging.Formatter('[%(reference_id)s] %(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(fmt)

        self.__logger.addHandler(ch)
        self.__logger.propagate = False

        self.__fluentd = fluentd.Fluentd()

    def __external(self, level, message):
        info = {
            "reference_id": reference.Reference().get(),
            "username": session.username(),
            "service": 'ztd.blunders-web',
            "module": self.__module,
            "timestamp": str(datetime.datetime.now()),
            "level": level,
            "message": message
        }

        self.__fluentd.log(info)

    def __internal(self, level, message):
        self.__logger.log(level, message, extra = {"reference_id": reference.Reference().get()})

    def info(self, message):
        self.__external(level = logging.INFO, message = message)
        self.__internal(level = logging.INFO, message = message)

    def error(self, message):
        self.__external(level = logging.ERROR, message = message)
        self.__internal(level = logging.ERROR, message = message)

    def traceback(self, e):
        traceback_text = ''.join(traceback.format_tb(e.__traceback__))
        self.__internal(level = logging.ERROR, message = traceback_text)
        traceback.print_tb(e.__traceback__)
