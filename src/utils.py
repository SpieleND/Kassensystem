from enum import Enum

from models.session import Session

class ROLES(Enum):
    system = "SYSTEM"
    admin = "admin"
    user = "user"
    guest = "guest"

session = Session()
