"""
认证路由
@author 结对小组
"""
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User
from utils.response import success, error

auth_bp = Blueprint('auth', __name__, url_prefix='/api/user')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return error('用户名和密码不能为空')
    
    if User.query.filter_by(username=data.get('username')).first():
        return error('用户名已存在')
    
    user = User(
        username=data.get('username'),
        real_name=data.get('real_name'),
        phone=data.get('phone'),
        role=0,
        status=1
    )
    user.set_password(data.get('password'))
    
    try:
        db.session.add(user)
        db.session.commit()
        return success(message='注册成功')
    except Exception as e:
        db.session.rollback()
        return error(f'注册失败: {str(e)}')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return error('用户名和密码不能为空')
    
    user = User.query.filter_by(username=data.get('username')).first()
    if not user or not user.check_password(data.get('password')):
        return error('用户名或密码错误')
    if user.status == 0:
        return error('用户已被禁用')
    
    token = create_access_token(identity=user.id)
    return success({'token': token, 'user': user.to_dict()}, message='登录成功')

@auth_bp.route('/info', methods=['GET'])
@jwt_required()
def get_user_info():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return error('用户不存在')
    return success(user.to_dict())
