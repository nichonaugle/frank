import logging
from datetime import datetime

# Define custom log levels
SUCCESS = 21
SPEAKING = 22
SENT = 23
RECIEVED = 24

logging.addLevelName(SUCCESS, "SUCCESS")
logging.addLevelName(SPEAKING, "SPEAKING")
logging.addLevelName(SENT, "SENT")
logging.addLevelName(RECIEVED, "RECIEVED")

# Define color codes for levels
COLORS = {
    "SUCCESS": "\033[92m",  # Green
    "SPEAKING": "\033[94m",  # Blue
    "DEBUG": "\033[90m",     # Grey
    "SENT": "\033[90m",     # Grey
    "RECIEVED": "\033[90m",     # Grey
    "INFO": "\033[96m",      # White
    "WARNING": "\033[93m",   # Yellow
    "ERROR": "\033[91m",     # Red
    "CRITICAL": "\033[95m",  # Magenta
    "RESET": "\033[0m",      # Reset color
    "ASC_TIME": "\033[90m",  # White
    "NAME": "\033[97m",      # Grey
}

# Custom formatter to add colors
class CustomFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        """Override formatTime to apply color to asctime."""
        asctime = datetime.fromtimestamp(record.created).strftime(datefmt or "%Y-%m-%d %H:%M:%S,%f")[:-3]
        return f"{COLORS['ASC_TIME']}{asctime}{COLORS['RESET']}"
    
    def format(self, record):
        log_color = COLORS.get(record.levelname, COLORS["RESET"])
        reset_color = COLORS["RESET"]
        asctime_color = COLORS["ASC_TIME"]
        name_color = COLORS["NAME"]
        record.asctime = f"{asctime_color}{self.formatTime(record)}{reset_color}"
        record.name = f"{name_color}{record.name}{reset_color}"
        record.levelname = f"{log_color}[{record.levelname}]{reset_color}"
        record.msg = f"{log_color}{record.msg}{reset_color}"
        return super().format(record)

# Add methods for custom levels to Logger
def success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS):
        self._log(SUCCESS, message, args, **kwargs)

def speaking(self, message, *args, **kwargs):
    if self.isEnabledFor(SPEAKING):
        self._log(SPEAKING, message, args, **kwargs)

def sent(self, message, *args, **kwargs):
    if self.isEnabledFor(SENT):
        self._log(SENT, message, args, **kwargs)

def recieved(self, message, *args, **kwargs):
    if self.isEnabledFor(RECIEVED):
        self._log(RECIEVED, message, args, **kwargs)

logging.Logger.success = success
logging.Logger.speaking = speaking
logging.Logger.sent = sent
logging.Logger.recieved = recieved

logger = logging.getLogger('main_logger')
logger.setLevel(logging.DEBUG)

# Create a formatter and attach it to the handlers
formatter = CustomFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

file_handler = logging.FileHandler('frank.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

"""# Log some messages
logger.success('This is a debug message')
logger.speaking('This is a debug message')
logger.sent('This is a sent message')
logger.recieved('This is a recieved message')
logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')"""

def get_logger(name="main_logger"):
    logger = logging.getLogger(name)
    if not logger.handlers:  # Prevent adding multiple handlers
        handler = logging.StreamHandler()
        formatter = CustomFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger