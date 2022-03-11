"""Файл для логов"""

import logging

logging.basicConfig(
    format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
    level=logging.INFO, filename="static/logs/logs.log"
)


def exception_hook(exctype, value, traceback):
    """
    :param exctype:
    :param value:
    :param traceback:
    :return:
    Функция перехвата непредвиденных ошибок
    """
    logging.error(locals())
