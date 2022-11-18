from enum import Enum


class RoleEnum(str, Enum):
    user = 'user'  # обычный пользователь
    master = 'master'  # исполнитель услуги
    manager = 'manager'  # менеджер сети
    admin = 'admin'  # администратор всей системы (суперпользователь)
