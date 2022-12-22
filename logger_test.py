import logging
from logging import Logger

class MyLogger(Logger):

    def __init__(self, name, *args, **kwargs):
        super(MyLogger, self).__init__(name, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        print("msg is", msg)
        super(MyLogger, self).log(level, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.log(logging.INFO, msg, *args, **kwargs)

logging.setLoggerClass(MyLogger)

my_logger = logging.getLogger("MyLogger")
print("my_logger type is", type(my_logger))
my_logger.log(logging.INFO, "hi")
my_logger.info("hi2")

logging.setLoggerClass(Logger)
base_logger = logging.getLogger("BaseLogger")
print("my_logger type is", type(base_logger))
