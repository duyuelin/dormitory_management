"""
统一响应工具
@author 结对小组
"""
from flask import jsonify

def success(data=None, message='success'):
    return jsonify({'code': 200, 'message': message, 'data': data})

def error(message='error', code=500):
    return jsonify({'code': code, 'message': message, 'data': None})

def unauthorized(message='请先登录'):
    return jsonify({'code': 401, 'message': message, 'data': None}), 401

def forbidden(message='无权限操作'):
    return jsonify({'code': 403, 'message': message, 'data': None}), 403
