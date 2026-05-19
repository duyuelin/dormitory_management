"""
模型初始化
@author 结对小组
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User

__all__ = ['db', 'User']
