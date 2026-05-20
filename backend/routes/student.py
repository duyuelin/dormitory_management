"""
学生路由
@author 结对小组
"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from models import db, Student
from utils.response import success, error
from utils.decorators import admin_required

student_bp = Blueprint('student', __name__, url_prefix='/api/student')


@student_bp.route('/list', methods=['GET'])
@jwt_required()
def get_student_list():
    keyword = request.args.get('keyword')
    status = request.args.get('status', type=int)
    query = Student.query
    if keyword:
        query = query.filter(
            db.or_(Student.name.contains(keyword), Student.student_id.contains(keyword))
        )
    if status is not None:
        query = query.filter_by(status=status)
    students = query.all()
    return success([s.to_dict() for s in students])


@student_bp.route('/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return error('学生不存在')
    return success(student.to_dict())


@student_bp.route('/add', methods=['POST'])
@jwt_required()
@admin_required
def add_student():
    data = request.get_json()
    if not data or not data.get('student_id') or not data.get('name'):
        return error('学号和姓名不能为空')

    if Student.query.filter_by(student_id=data.get('student_id')).first():
        return error('学号已存在')

    student = Student(
        student_id=data.get('student_id'),
        name=data.get('name'),
        gender=data.get('gender'),
        phone=data.get('phone'),
        email=data.get('email'),
        college=data.get('college'),
        major=data.get('major'),
        class_name=data.get('class_name'),
        grade=data.get('grade'),
        status=2
    )

    try:
        db.session.add(student)
        db.session.commit()
        return success(message='添加成功')
    except Exception as e:
        db.session.rollback()
        return error(f'添加失败: {str(e)}')


@student_bp.route('/update', methods=['PUT'])
@jwt_required()
@admin_required
def update_student():
    data = request.get_json()
    if not data or not data.get('id'):
        return error('学生ID不能为空')

    student = Student.query.get(data.get('id'))
    if not student:
        return error('学生不存在')

    student.name = data.get('name', student.name)
    student.gender = data.get('gender', student.gender)
    student.phone = data.get('phone', student.phone)
    student.email = data.get('email', student.email)
    student.college = data.get('college', student.college)
    student.major = data.get('major', student.major)
    student.class_name = data.get('class_name', student.class_name)
    student.grade = data.get('grade', student.grade)
    student.status = data.get('status', student.status)

    try:
        db.session.commit()
        return success(message='更新成功')
    except Exception as e:
        db.session.rollback()
        return error(f'更新失败: {str(e)}')


@student_bp.route('/delete/<int:student_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return error('学生不存在')

    try:
        db.session.delete(student)
        db.session.commit()
        return success(message='删除成功')
    except Exception as e:
        db.session.rollback()
        return error(f'删除失败: {str(e)}')
