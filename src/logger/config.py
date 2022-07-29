from enum import Enum


class TargetType(Enum):
    NO_TYPE = 0
    BOT = 1
    ADMIN = 2


LOG_FOLDER = 'log'

LOG_BOT_LEVEL = 'INFO'
LOG_BOT_FILE = 'bot.log'
LOG_ADMIN_LEVEL = 'INFO'
LOG_ADMIN_FILE = 'admin.log'
