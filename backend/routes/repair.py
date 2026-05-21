"""
报修管理路由
@author 结对小组
"""
from datetime import datetime
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Room, RepairRecord
from utils.response import success, error
from utils.decorators import admin_required

repair_bp = Blueprint('repair', __name__, url_prefix='/api/repair')


@repair_bp.route('/list', methods=['GET'])
@jwt_required()
def get_repair_list():
    status = request.args.get('status', type=int)
    query = RepairRecord.query.order_by(RepairRecord.create_time.desc())
    if status is not None:
        query = query.filter_by(status=status)
    records = query.all()
    return success([r.to_dict() for r in records])


@repair_bp.route('/submit', methods=['POST'])
@jwt_required()
@admin_required
def submit_repair():
    data = request.get_json()
    if not data or not data.get('room_id') or not data.get('repair_type'):
        return error('房间ID和报修类型不能为空')

    room = Room.query.get(data.get('room_id'))
    if not room:
        return error('房间不存在')

    repair = RepairRecord(
        room_id=data.get('room_id'),
        student_id=data.get('student_id'),
        repair_type=data.get('repair_type'),
        description=data.get('description'),
        contact_phone=data.get('contact_phone'),
        status=0
    )

    try:
        db.session.add(repair)
        db.session.commit()
        return success(message='报修提交成功')
    except Exception as e:
        db.session.rollback()
        return error(f'提交失败: {str(e)}')


@repair_bp.route('/handle/<int:repair_id>', methods=['POST'])
@jwt_required()
@admin_required
def handle_repair(repair_id):
    repair = RepairRecord.query.get(repair_id)
    if not repair:
        return error('报修记录不存在')

    data = request.get_json()

    try:
        repair.status = data.get('status', repair.status)
        repair.handle_result = data.get('handle_result', repair.handle_result)
        repair.handle_time = datetime.now()

        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        repair.handler = user.real_name if user else '管理员'

        db.session.commit()
        return success(message='处理成功')
    except Exception as e:
        db.session.rollback()
        return error(f'处理失败: {str(e)}')


@repair_bp.route('/delete/<int:repair_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_repair(repair_id):
    repair = RepairRecord.query.get(repair_id)
    if not repair:
        return error('报修记录不存在')

    try:
        db.session.delete(repair)
        db.session.commit()
        return success(message='删除成功')
    except Exception as e:
        db.session.rollback()
        return error(f'删除失败: {str(e)}')
