"""
报修记录模型
@author 结对小组
"""
from datetime import datetime
from . import db


class RepairRecord(db.Model):
    """报修记录表"""
    __tablename__ = 'repair_record'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    repair_type = db.Column(db.String(50))  # 报修类型：水电/门窗/空调/网络/家具
    description = db.Column(db.Text)  # 报修描述
    contact_phone = db.Column(db.String(20))  # 联系电话
    status = db.Column(db.SmallInteger, default=0)  # 0-待处理, 1-处理中, 2-已完成
    handle_result = db.Column(db.Text)  # 处理结果
    handle_time = db.Column(db.DateTime)  # 处理时间
    handler = db.Column(db.String(50))  # 处理人
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    room = db.relationship('Room', backref='repairs')
    student = db.relationship('Student', backref='repairs')

    def to_dict(self):
        return {
            'id': self.id,
            'room_id': self.room_id,
            'room_number': self.room.room_number if self.room else None,
            'student_id': self.student_id,
            'student_name': self.student.name if self.student else None,
            'repair_type': self.repair_type,
            'description': self.description,
            'contact_phone': self.contact_phone,
            'status': self.status,
            'handle_result': self.handle_result,
            'handle_time': self.handle_time.strftime('%Y-%m-%d %H:%M:%S') if self.handle_time else None,
            'handler': self.handler,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None
        }
