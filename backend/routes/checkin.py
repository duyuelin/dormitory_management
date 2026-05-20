"""
入住管理路由
@author 结对小组
"""
from datetime import date
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from models import db, Student, Room, CheckInRecord
from utils.response import success, error
from utils.decorators import admin_required

checkin_bp = Blueprint('checkin', __name__, url_prefix='/api/checkin')


@checkin_bp.route('/list', methods=['GET'])
@jwt_required()
def get_checkin_list():
    records = CheckInRecord.query.order_by(CheckInRecord.create_time.desc()).all()
    return success([r.to_dict() for r in records])


@checkin_bp.route('/check-in', methods=['POST'])
@jwt_required()
@admin_required
def check_in():
    data = request.get_json()
    if not data or not data.get('student_id') or not data.get('room_id'):
        return error('学生ID和房间ID不能为空')

    student = Student.query.get(data.get('student_id'))
    if not student:
        return error('学生不存在')
    if student.status == 1:
        return error('该学生已入住')

    room = Room.query.get(data.get('room_id'))
    if not room:
        return error('房间不存在')
    if room.available_beds <= 0:
        return error('该房间已满')

    bed_number = data.get('bed_number', 1)
    occupied = CheckInRecord.query.filter_by(room_id=room.id, bed_number=bed_number, status=1).first()
    if occupied:
        return error('该床位已被占用')

    record = CheckInRecord(
        student_id=student.id,
        room_id=room.id,
        bed_number=bed_number,
        check_in_date=date.today(),
        status=1
    )

    try:
        room.available_beds -= 1
        if room.available_beds == 0:
            room.status = 2
        student.status = 1
        db.session.add(record)
        db.session.commit()
        return success(message='入住成功')
    except Exception as e:
        db.session.rollback()
        return error(f'入住失败: {str(e)}')


@checkin_bp.route('/check-out/<int:record_id>', methods=['POST'])
@jwt_required()
@admin_required
def check_out(record_id):
    record = CheckInRecord.query.get(record_id)
    if not record:
        return error('入住记录不存在')
    if record.status == 0:
        return error('该记录已退宿')

    try:
        record.status = 0
        record.check_out_date = date.today()

        room = record.room
        room.available_beds += 1
        room.status = 1

        student = record.student
        student.status = 0

        db.session.commit()
        return success(message='退宿成功')
    except Exception as e:
        db.session.rollback()
        return error(f'退宿失败: {str(e)}')


@checkin_bp.route('/student/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student_checkin(student_id):
    records = CheckInRecord.query.filter_by(student_id=student_id).order_by(CheckInRecord.create_time.desc()).all()
    return success([r.to_dict() for r in records])
