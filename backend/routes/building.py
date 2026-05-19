"""
宿舍楼路由
@author 结对小组
"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from models import db, Building, Room
from utils.response import success, error
from utils.decorators import admin_required

building_bp = Blueprint('building', __name__, url_prefix='/api/building')

@building_bp.route('/list', methods=['GET'])
@jwt_required()
def get_building_list():
    buildings = Building.query.all()
    return success([b.to_dict() for b in buildings])

@building_bp.route('/<int:building_id>', methods=['GET'])
@jwt_required()
def get_building(building_id):
    building = Building.query.get(building_id)
    if not building:
        return error('宿舍楼不存在')
    return success(building.to_dict())

@building_bp.route('/add', methods=['POST'])
@jwt_required()
@admin_required
def add_building():
    data = request.get_json()
    if not data or not data.get('name'):
        return error('楼名不能为空')
    
    building = Building(
        name=data.get('name'),
        code=data.get('code'),
        floors=data.get('floors', 6),
        rooms_per_floor=data.get('rooms_per_floor', 20),
        total_beds=data.get('total_beds', 0),
        available_beds=data.get('available_beds', 0),
        manager=data.get('manager'),
        manager_phone=data.get('manager_phone'),
        gender=data.get('gender'),
        status=1
    )
    
    try:
        db.session.add(building)
        db.session.commit()
        return success(message='添加成功')
    except Exception as e:
        db.session.rollback()
        return error(f'添加失败: {str(e)}')

@building_bp.route('/update', methods=['PUT'])
@jwt_required()
@admin_required
def update_building():
    data = request.get_json()
    if not data or not data.get('id'):
        return error('宿舍楼ID不能为空')
    
    building = Building.query.get(data.get('id'))
    if not building:
        return error('宿舍楼不存在')
    
    building.name = data.get('name', building.name)
    building.code = data.get('code', building.code)
    building.floors = data.get('floors', building.floors)
    building.manager = data.get('manager', building.manager)
    building.manager_phone = data.get('manager_phone', building.manager_phone)
    building.gender = data.get('gender', building.gender)
    
    try:
        db.session.commit()
        return success(message='更新成功')
    except Exception as e:
        db.session.rollback()
        return error(f'更新失败: {str(e)}')

@building_bp.route('/delete/<int:building_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_building(building_id):
    building = Building.query.get(building_id)
    if not building:
        return error('宿舍楼不存在')
    
    try:
        db.session.delete(building)
        db.session.commit()
        return success(message='删除成功')
    except Exception as e:
        db.session.rollback()
        return error(f'删除失败: {str(e)}')

@building_bp.route('/<int:building_id>/rooms', methods=['GET'])
@jwt_required()
def get_building_rooms(building_id):
    rooms = Room.query.filter_by(building_id=building_id).all()
    return success([r.to_dict() for r in rooms])
