from enum import Enum
import os


class EntityType(Enum):
    NO_TYPE = 0
    TENANT = 1
    LANDLORD = 2
    FLAT = 3


API_TOKEN = os.getenv('HOSTEL_TOKEN_API')

IMG_PATH = './img'
