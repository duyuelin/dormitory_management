"""
装饰器工具
@author 结对小组
"""
from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from models import User
from utils.response import unauthorized, forbidden

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except:
            return unauthorized()
    return wrapper

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(int(user_id))
            if not user or user.role != 1:
                return forbidden()
            return fn(*args, **kwargs)
        except:
            return unauthorized()
    return wrapper
