from enum import Enum


class UserRole(Enum, str):
    ADMIN = "admin"
    USER = "user"
