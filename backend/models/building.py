"""
宿舍楼模型
@author 结对小组
"""
from datetime import datetime
from . import db

class Building(db.Model):
    """宿舍楼表"""
    __tablename__ = 'building'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)  # 楼名，如：1号楼
    code = db.Column(db.String(20), unique=True)  # 楼号编码
    floors = db.Column(db.Integer, default=6)  # 楼层数
    rooms_per_floor = db.Column(db.Integer, default=20)  # 每层房间数
    total_beds = db.Column(db.Integer, default=0)  # 总床位数
    available_beds = db.Column(db.Integer, default=0)  # 空余床位
    manager = db.Column(db.String(50))  # 宿管姓名
    manager_phone = db.Column(db.String(20))  # 宿管电话
    gender = db.Column(db.String(10))  # 男宿/女宿
    status = db.Column(db.SmallInteger, default=1)  # 0-停用, 1-正常
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关联房间
    rooms = db.relationship('Room', backref='building', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'floors': self.floors,
            'rooms_per_floor': self.rooms_per_floor,
            'total_beds': self.total_beds,
            'available_beds': self.available_beds,
            'manager': self.manager,
            'manager_phone': self.manager_phone,
            'gender': self.gender,
            'status': self.status,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None
        }
