from enum import Enum
import os


class EntityType(Enum):
    NO_TYPE = 0
    TENANT = 1
    LANDLORD = 2
    FLAT = 3
    NEIGHBORHOOD = 4
    GOODS = 5

    def __eq__(self, other):
        if self.__class__ is other.__class__ and self.value == other.value:
            return True
        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.value)


API_TOKEN = os.getenv('HOSTEL_TOKEN_API')

IMG_PATH = './img'
