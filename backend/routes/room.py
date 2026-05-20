"""
房间路由
@author 结对小组
"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from models import db, Building, Room
from utils.response import success, error
from utils.decorators import admin_required

room_bp = Blueprint('room', __name__, url_prefix='/api/room')


@room_bp.route('/list', methods=['GET'])
@jwt_required()
def get_room_list():
    status = request.args.get('status', type=int)
    query = Room.query
    if status is not None:
        query = query.filter_by(status=status)
    rooms = query.all()
    return success([r.to_dict() for r in rooms])


@room_bp.route('/available', methods=['GET'])
@jwt_required()
def get_available_rooms():
    rooms = Room.query.filter(Room.available_beds > 0, Room.status == 1).all()
    return success([r.to_dict() for r in rooms])


@room_bp.route('/<int:room_id>', methods=['GET'])
@jwt_required()
def get_room(room_id):
    room = Room.query.get(room_id)
    if not room:
        return error('房间不存在')
    return success(room.to_dict())


@room_bp.route('/add', methods=['POST'])
@jwt_required()
@admin_required
def add_room():
    data = request.get_json()
    if not data or not data.get('building_id') or not data.get('room_number'):
        return error('宿舍楼ID和房间号不能为空')

    building = Building.query.get(data.get('building_id'))
    if not building:
        return error('宿舍楼不存在')

    room = Room(
        building_id=data.get('building_id'),
        room_number=data.get('room_number'),
        floor=data.get('floor', 1),
        total_beds=data.get('total_beds', 4),
        available_beds=data.get('available_beds', data.get('total_beds', 4)),
        room_type=data.get('room_type', '四人间'),
        price=data.get('price', 1200),
        status=1
    )

    try:
        building.total_beds += room.total_beds
        building.available_beds += room.available_beds
        db.session.add(room)
        db.session.commit()
        return success(message='添加成功')
    except Exception as e:
        db.session.rollback()
        return error(f'添加失败: {str(e)}')


@room_bp.route('/update', methods=['PUT'])
@jwt_required()
@admin_required
def update_room():
    data = request.get_json()
    if not data or not data.get('id'):
        return error('房间ID不能为空')

    room = Room.query.get(data.get('id'))
    if not room:
        return error('房间不存在')

    old_total = room.total_beds
    old_available = room.available_beds

    room.room_number = data.get('room_number', room.room_number)
    room.floor = data.get('floor', room.floor)
    room.total_beds = data.get('total_beds', room.total_beds)
    room.available_beds = data.get('available_beds', room.available_beds)
    room.room_type = data.get('room_type', room.room_type)
    room.price = data.get('price', room.price)
    room.status = data.get('status', room.status)

    try:
        building = room.building
        building.total_beds += room.total_beds - old_total
        building.available_beds += room.available_beds - old_available
        db.session.commit()
        return success(message='更新成功')
    except Exception as e:
        db.session.rollback()
        return error(f'更新失败: {str(e)}')


@room_bp.route('/delete/<int:room_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_room(room_id):
    room = Room.query.get(room_id)
    if not room:
        return error('房间不存在')

    try:
        building = room.building
        building.total_beds -= room.total_beds
        building.available_beds -= room.available_beds
        db.session.delete(room)
        db.session.commit()
        return success(message='删除成功')
    except Exception as e:
        db.session.rollback()
        return error(f'删除失败: {str(e)}')
