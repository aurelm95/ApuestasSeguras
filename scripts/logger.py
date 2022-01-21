import logging

# https://stackoverflow.com/questions/1343227/can-pythons-logging-format-be-modified-depending-on-the-message-log-level
# por mirar:
# https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output 
class MyFormatter(logging.Formatter):

    ROJO=     "\033[31;1;1m"
    AMARILLO= "\033[33;1;1m"
    AZUL=     "\033[34;1;1m"
    RESET=    "\033[0m"

    BASE_FORMAT='%(asctime)s: %(name)s.py: [%(levelname)s]: %(message)s'
    BASE_FORMAT='%(name)s.py: [%(levelname)s]: %(message)s'

    def __init__(self, fmt=''):
        logging.Formatter.__init__(self, fmt)

    def format(self, record):
        colored_base_format=MyFormatter.BASE_FORMAT

        if record.levelno == logging.DEBUG:
            colored_base_format = MyFormatter.AZUL+MyFormatter.BASE_FORMAT+MyFormatter.RESET

        elif record.levelno == logging.WARNING:
            colored_base_format = MyFormatter.AMARILLO+MyFormatter.BASE_FORMAT+MyFormatter.RESET

        elif record.levelno == logging.ERROR:
            colored_base_format = MyFormatter.ROJO+MyFormatter.BASE_FORMAT+MyFormatter.RESET

        result = logging.Formatter(colored_base_format).format(record)

        return result

apuestas_logger = logging.getLogger(__name__)
apuestas_logger.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s: %(name)s.py: [%(levelname)s]: %(message)s',"%H:%M:%S")
# Custom formatter

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(MyFormatter())
apuestas_logger.addHandler(stream_handler)




if __name__=='__main__':
    apuestas_logger.info("info")
    apuestas_logger.warning("warning")
    apuestas_logger.debug("debug")
    apuestas_logger.error("error")

