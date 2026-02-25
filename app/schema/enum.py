from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    employee = "employee"
    user = "user"