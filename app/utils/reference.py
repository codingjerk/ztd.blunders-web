import uuid

from functools import update_wrapper

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Reference(metaclass = Singleton):
    __reference = None

    def __init__(self):
        pass

    def create(self):
        self.__reference = uuid.uuid4().hex

    def get(self):
        return self.__reference

    def clean(self):
        self.__reference = None
