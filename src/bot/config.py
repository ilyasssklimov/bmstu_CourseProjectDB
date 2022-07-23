from enum import Enum
import os


class EntityTypes(Enum):
    TENANT = 1
    LANDLORD = 2
    FLAT = 3


API_TOKEN = os.getenv('BOT_API')

LOG_LEVEL = 'INFO'
LOG_FOLDER = 'log'
LOG_NAME_FILE = 'bot.log'

IMG_PATH = './img'

