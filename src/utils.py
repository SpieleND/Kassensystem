from enum import Enum

from models.session import Session

class ROLES(Enum):
    SYSTEM = 1
    admin = 2
    user = 3
    guest = 4

session = Session()
