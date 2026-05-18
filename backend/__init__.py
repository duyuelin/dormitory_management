"""
模型初始化
@author 结对小组
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .building import Building
from .room import Room
from .student import Student
from .checkin import CheckInRecord
from .repair import RepairRecord

__all__ = ['db', 'User', 'Building', 'Room', 'Student', 'CheckInRecord', 'RepairRecord']
