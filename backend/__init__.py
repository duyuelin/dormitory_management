"""
模型初始化
@author 结对小组
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# backend/models/__init__.py
from app import db  # 从 app.py 导入 db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
from .user import User
from .building import Building
from .room import Room
from .student import Student
from .checkin import CheckInRecord
from .repair import RepairRecord

__all__ = ['db', 'User', 'Building', 'Room', 'Student', 'CheckInRecord', 'RepairRecord']
