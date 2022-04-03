import logging
import os

# https://stackoverflow.com/questions/1343227/can-pythons-logging-format-be-modified-depending-on-the-message-log-level
# por mirar:
# https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output 
class MyFormatter(logging.Formatter):

    # Mas colores:
    # https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
    # https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
    ROJO=     "\033[31;1;1m"
    AMARILLO= "\033[33;1;1m"
    AZUL=     "\033[34;1;1m"
    NARANJA = "\033[38;5;166m"
    RJ_NG=    "\033[30;41m" # fondo rojo con texto negro
    RESET=    "\033[0m"

    BASE_FORMAT='%(asctime)s: %(name)s.py: [%(levelname)s]: %(message)s'
    BASE_FORMAT='%(name)s.py: [%(levelname)s]: %(message)s'
    BASE_FORMAT='%(pathname)-40s: [%(levelname)s]: %(message)s'

    def __init__(self, fmt=''):
        logging.Formatter.__init__(self, fmt)

    def format(self, record):
        colored_base_format=MyFormatter.BASE_FORMAT

        list_path=os.path.realpath(record.pathname).split(os.sep)
        list_path=list_path[list_path.index('ApuestasSeguras'):]
        record.pathname=os.path.join(*list_path)

        if record.levelno == logging.TIMESTAMP_WARNING:
            colored_base_format = MyFormatter.NARANJA+MyFormatter.BASE_FORMAT+MyFormatter.RESET

        elif record.levelno == logging.DEBUG:
            colored_base_format = MyFormatter.AZUL+MyFormatter.BASE_FORMAT+MyFormatter.RESET

        elif record.levelno == logging.WARNING:
            colored_base_format = MyFormatter.AMARILLO+MyFormatter.BASE_FORMAT+MyFormatter.RESET

        elif record.levelno == logging.ERROR:
            colored_base_format = MyFormatter.ROJO+MyFormatter.BASE_FORMAT+MyFormatter.RESET
        
        elif record.levelno == logging.CRITICAL:
            colored_base_format = MyFormatter.RJ_NG+MyFormatter.BASE_FORMAT+MyFormatter.RESET

        result = logging.Formatter(colored_base_format).format(record)

        return result

# Añadir nuevo nivel de logging
# https://stackoverflow.com/questions/2183233/how-to-add-a-custom-loglevel-to-pythons-logging-facility/35804945#35804945
levelName="TIMESTAMP_WARNING"
levelNum=logging.DEBUG-5 # =5
methodName='timestamp_warning'

def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)

def logToRoot(message, *args, **kwargs):
    logging.log(levelNum, message, *args, **kwargs)

logging.addLevelName(levelNum, levelName)
setattr(logging, levelName, levelNum)
setattr(logging.getLoggerClass(), methodName, logForLevel)
setattr(logging, methodName, logToRoot)

# Inicializacion
apuestas_logger = logging.getLogger(__name__)
apuestas_logger.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s: %(name)s.py: [%(levelname)s]: %(message)s',"%H:%M:%S")

# Custom formatter
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(MyFormatter())
apuestas_logger.addHandler(stream_handler)

# De los siguientes enlaces se pueden sacar buenos comandos para el formato
# https://stackoverflow.com/questions/533048/how-to-log-source-file-name-and-line-number-in-python
# https://stackoverflow.com/questions/28644821/how-to-specify-caller-file-name-in-python-logger/30257387

# Del siguiente enlace se puede sacar como hacer que se pueda recortar el pathname para el logger
# https://stackify.dev/323830-python-logging-how-do-i-truncate-the-pathname-to-just-the-last-few-characters

if __name__=='__main__':
    apuestas_logger.timestamp_warning("timestamp warning")
    apuestas_logger.debug("debug")
    apuestas_logger.info("info")
    apuestas_logger.warning("warning")
    apuestas_logger.error("error")
    apuestas_logger.critical("critical")
    

