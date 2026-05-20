"""
房间模型
@author 结对小组
"""
from datetime import datetime
from . import db

class Room(db.Model):
    """房间表"""
    __tablename__ = 'room'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'), nullable=False)
    room_number = db.Column(db.String(20), nullable=False)  # 房间号，如：101
    floor = db.Column(db.Integer)  # 楼层
    total_beds = db.Column(db.Integer, default=4)  # 总床位数
    available_beds = db.Column(db.Integer, default=4)  # 空余床位
    room_type = db.Column(db.String(20), default='四人间')  # 房间类型
    price = db.Column(db.Float, default=1200.0)  # 住宿费/学期
    status = db.Column(db.SmallInteger, default=1)  # 0-停用, 1-正常, 2-已满
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关联入住记录
    checkins = db.relationship('CheckInRecord', backref='room', lazy='dynamic')
      
    def to_dict(self):
        return {
            'id': self.id,
            'building_id': self.building_id,
            'building_name': self.building.name if self.building else None,
            'room_number': self.room_number,
            'floor': self.floor,
            'total_beds': self.total_beds,
            'available_beds': self.available_beds,
            'room_type': self.room_type,
            'price': float(self.price) if self.price else 0,
            'status': self.status,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None
        }
