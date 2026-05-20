"""
入住记录模型
@author 结对小组
"""
from datetime import datetime, date
from . import db


class CheckInRecord(db.Model):
    """入住记录表"""
    __tablename__ = 'checkin_record'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    bed_number = db.Column(db.Integer)  # 床位号
    check_in_date = db.Column(db.Date, default=date.today)  # 入住日期
    check_out_date = db.Column(db.Date)  # 退宿日期
    status = db.Column(db.SmallInteger, default=1)  # 0-已退宿, 1-在住
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    student = db.relationship('Student', backref='checkins')
    # room 关系由 Room.checkins 的 backref 自动创建，无需重复定义

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'student_name': self.student.name if self.student else None,
            'room_id': self.room_id,
            'room_number': self.room.room_number if self.room else None,
            'bed_number': self.bed_number,
            'check_in_date': self.check_in_date.strftime('%Y-%m-%d') if self.check_in_date else None,
            'check_out_date': self.check_out_date.strftime('%Y-%m-%d') if self.check_out_date else None,
            'status': self.status,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None
        }
