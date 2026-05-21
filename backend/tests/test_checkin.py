"""
入住管理模块测试代码
@author 结对小组 - 后端测试
@cross-testing duyuelin 交叉测试验证通过 (2026-05-21)
"""
import unittest
import json
import sys
import os
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User, Building, Room, Student, CheckInRecord


class CheckInTestCase(unittest.TestCase):
    """入住管理模块测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.app = create_app('testing')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            # 创建管理员用户
            admin = User(username='admin', real_name='管理员', role=1)
            admin.set_password('admin123')
            db.session.add(admin)
            
            # 创建测试数据
            building = Building(name='1号楼', code='B001', total_beds=4, available_beds=4)
            db.session.add(building)
            db.session.flush()
            
            room = Room(
                building_id=building.id,
                room_number='101',
                total_beds=4,
                available_beds=4,
                status=1
            )
            db.session.add(room)
            db.session.flush()
            
            student = Student(
                student_id='2024001001',
                name='张三',
                status=2  # 待入住
            )
            db.session.add(student)
            db.session.flush()
            
            self.room_id = room.id
            self.student_id = student.id
            db.session.commit()
            
            self.admin_token = self._get_token('admin', 'admin123')
    
    def _get_token(self, username, password):
        """获取登录token"""
        response = self.client.post('/api/user/login',
            data=json.dumps({'username': username, 'password': password}),
            content_type='application/json'
        )
        return json.loads(response.data)['data']['token']
    
    def tearDown(self):
        """测试后清理"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_get_checkin_list(self):
        """测试获取入住记录列表"""
        # 先创建一个入住记录
        with self.app.app_context():
            record = CheckInRecord(
                student_id=self.student_id,
                room_id=self.room_id,
                bed_number=1,
                check_in_date=date.today(),
                status=1
            )
            db.session.add(record)
            db.session.commit()
        
        response = self.client.get('/api/checkin/list',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        self.assertEqual(len(data['data']), 1)
    
    def test_check_in_success(self):
        """测试办理入住成功"""
        response = self.client.post('/api/checkin/check-in',
            data=json.dumps({
                'student_id': self.student_id,
                'room_id': self.room_id,
                'bed_number': 1
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['message'], '入住成功')
        
        # 验证房间和学生状态更新
        with self.app.app_context():
            room = Room.query.get(self.room_id)
            student = Student.query.get(self.student_id)
            self.assertEqual(room.available_beds, 3)
            self.assertEqual(student.status, 1)  # 在住
    
    def test_check_in_without_required_fields(self):
        """测试办理入住缺少必填字段"""
        response = self.client.post('/api/checkin/check-in',
            data=json.dumps({'student_id': self.student_id}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 500)
        self.assertIn('不能为空', data['message'])
    
    def test_check_in_already_checked_in(self):
        """测试已入住学生再次办理入住"""
        # 先将学生状态设为在住
        with self.app.app_context():
            student = Student.query.get(self.student_id)
            student.status = 1
            db.session.commit()
        
        response = self.client.post('/api/checkin/check-in',
            data=json.dumps({
                'student_id': self.student_id,
                'room_id': self.room_id,
                'bed_number': 1
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 500)
        self.assertIn('已入住', data['message'])
    
    def test_check_in_full_room(self):
        """测试已满房间办理入住"""
        # 将房间设为已满
        with self.app.app_context():
            room = Room.query.get(self.room_id)
            room.available_beds = 0
            room.status = 2
            db.session.commit()
        
        response = self.client.post('/api/checkin/check-in',
            data=json.dumps({
                'student_id': self.student_id,
                'room_id': self.room_id,
                'bed_number': 1
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 500)
        self.assertIn('已满', data['message'])
    
    def test_check_in_occupied_bed(self):
        """测试占用已被占用的床位"""
        # 先创建一个入住记录
        with self.app.app_context():
            record = CheckInRecord(
                student_id=self.student_id,
                room_id=self.room_id,
                bed_number=1,
                check_in_date=date.today(),
                status=1
            )
            db.session.add(record)
            db.session.commit()
            
            # 创建另一个待入住学生
            student2 = Student(student_id='2024001002', name='李四', status=2)
            db.session.add(student2)
            db.session.commit()
        
        response = self.client.post('/api/checkin/check-in',
            data=json.dumps({
                'student_id': 2,
                'room_id': self.room_id,
                'bed_number': 1
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 500)
        self.assertIn('床位已被占用', data['message'])
    
    def test_check_out_success(self):
        """测试办理退宿成功"""
        # 先创建入住记录
        with self.app.app_context():
            record = CheckInRecord(
                student_id=self.student_id,
                room_id=self.room_id,
                bed_number=1,
                check_in_date=date.today(),
                status=1
            )
            db.session.add(record)
            
            room = Room.query.get(self.room_id)
            room.available_beds = 3
            
            student = Student.query.get(self.student_id)
            student.status = 1
            db.session.commit()
            record_id = record.id
        
        response = self.client.post(f'/api/checkin/check-out/{record_id}',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['message'], '退宿成功')
        
        # 验证状态更新
        with self.app.app_context():
            record = CheckInRecord.query.get(record_id)
            room = Room.query.get(self.room_id)
            student = Student.query.get(self.student_id)
            self.assertEqual(record.status, 0)  # 已退宿
            self.assertEqual(room.available_beds, 4)
            self.assertEqual(student.status, 0)  # 退宿
    
    def test_check_out_already_checked_out(self):
        """测试已退宿再次办理退宿"""
        # 创建已退宿的记录
        with self.app.app_context():
            record = CheckInRecord(
                student_id=self.student_id,
                room_id=self.room_id,
                bed_number=1,
                check_in_date=date.today(),
                status=0  # 已退宿
            )
            db.session.add(record)
            db.session.commit()
            record_id = record.id
        
        response = self.client.post(f'/api/checkin/check-out/{record_id}',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 500)
        self.assertIn('已退宿', data['message'])
    
    def test_get_student_checkin(self):
        """测试获取学生入住记录"""
        # 创建入住记录
        with self.app.app_context():
            record = CheckInRecord(
                student_id=self.student_id,
                room_id=self.room_id,
                bed_number=1,
                check_in_date=date.today(),
                status=1
            )
            db.session.add(record)
            db.session.commit()
        
        response = self.client.get(f'/api/checkin/student/{self.student_id}',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        self.assertEqual(len(data['data']), 1)


class CheckInModelTestCase(unittest.TestCase):
    """入住记录模型测试类"""
    
    def setUp(self):
        self.app = create_app('testing')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with self.app.app_context():
            db.create_all()
            # 创建基础数据
            building = Building(name='1号楼', code='B001')
            db.session.add(building)
            db.session.flush()
            
            room = Room(building_id=building.id, room_number='101', total_beds=4, available_beds=4)
            db.session.add(room)
            db.session.flush()
            
            student = Student(student_id='2024001001', name='张三')
            db.session.add(student)
            db.session.flush()
            
            self.room_id = room.id
            self.student_id = student.id
            db.session.commit()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_checkin_record_creation(self):
        """测试入住记录创建"""
        with self.app.app_context():
            record = CheckInRecord(
                student_id=self.student_id,
                room_id=self.room_id,
                bed_number=1,
                check_in_date=date.today(),
                status=1
            )
            db.session.add(record)
            db.session.commit()
            
            self.assertIsNotNone(record.id)
            self.assertEqual(record.bed_number, 1)
            self.assertEqual(record.status, 1)
    
    def test_checkin_record_to_dict(self):
        """测试入住记录模型转字典"""
        with self.app.app_context():
            record = CheckInRecord(
                student_id=self.student_id,
                room_id=self.room_id,
                bed_number=1,
                check_in_date=date.today(),
                status=1
            )
            db.session.add(record)
            db.session.commit()
            
            record_dict = record.to_dict()
            self.assertEqual(record_dict['bed_number'], 1)
            self.assertEqual(record_dict['status'], 1)
            self.assertIn('student_name', record_dict)
            self.assertIn('room_number', record_dict)


def run_tests():
    """运行测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(CheckInTestCase))
    suite.addTests(loader.loadTestsFromTestCase(CheckInModelTestCase))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
