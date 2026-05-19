"""
报修管理模块测试代码
@author 结对小组 - 后端测试
"""
import unittest
import json
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User, Building, Room, Student, RepairRecord


class RepairTestCase(unittest.TestCase):
    """报修管理模块测试类"""
    
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
    
    def test_get_repair_list(self):
        """测试获取报修记录列表"""
        # 创建报修记录
        with self.app.app_context():
            repair = RepairRecord(
                room_id=self.room_id,
                student_id=self.student_id,
                repair_type='水电',
                description='灯不亮了',
                contact_phone='13800138001',
                status=0
            )
            db.session.add(repair)
            db.session.commit()
        
        response = self.client.get('/api/repair/list',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['repair_type'], '水电')
    
    def test_get_repair_list_with_status(self):
        """测试按状态筛选报修记录"""
        # 创建不同状态的报修记录
        with self.app.app_context():
            repair1 = RepairRecord(room_id=self.room_id, repair_type='水电', status=0)
            repair2 = RepairRecord(room_id=self.room_id, repair_type='门窗', status=1)
            db.session.add_all([repair1, repair2])
            db.session.commit()
        
        response = self.client.get('/api/repair/list?status=1',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['repair_type'], '门窗')
    
    def test_submit_repair_success(self):
        """测试提交报修成功"""
        response = self.client.post('/api/repair/submit',
            data=json.dumps({
                'room_id': self.room_id,
                'student_id': self.student_id,
                'repair_type': '空调',
                'description': '空调不制冷',
                'contact_phone': '13800138001'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['message'], '报修提交成功')
        
        # 验证报修记录创建
        with self.app.app_context():
            repair = RepairRecord.query.filter_by(room_id=self.room_id).first()
            self.assertIsNotNone(repair)
            self.assertEqual(repair.status, 0)  # 待处理
    
    def test_submit_repair_without_room(self):
        """测试提交报修缺少房间ID"""
        response = self.client.post('/api/repair/submit',
            data=json.dumps({'repair_type': '水电'}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 500)
        self.assertIn('不能为空', data['message'])
    
    def test_submit_repair_nonexistent_room(self):
        """测试提交报修不存在的房间"""
        response = self.client.post('/api/repair/submit',
            data=json.dumps({'room_id': 999, 'repair_type': '水电'}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 500)
        self.assertIn('不存在', data['message'])
    
    def test_handle_repair_success(self):
        """测试处理报修成功"""
        # 创建报修记录
        with self.app.app_context():
            repair = RepairRecord(
                room_id=self.room_id,
                repair_type='水电',
                description='灯不亮',
                status=0
            )
            db.session.add(repair)
            db.session.commit()
            repair_id = repair.id
        
        response = self.client.post(f'/api/repair/handle/{repair_id}',
            data=json.dumps({
                'status': 2,  # 已完成
                'handle_result': '已更换灯泡'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['message'], '处理成功')
        
        # 验证报修记录更新
        with self.app.app_context():
            repair = RepairRecord.query.get(repair_id)
            self.assertEqual(repair.status, 2)
            self.assertEqual(repair.handle_result, '已更换灯泡')
            self.assertIsNotNone(repair.handle_time)
            self.assertEqual(repair.handler, '管理员')
    
    def test_handle_nonexistent_repair(self):
        """测试处理不存在的报修记录"""
        response = self.client.post('/api/repair/handle/999',
            data=json.dumps({'status': 1}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 500)
        self.assertIn('不存在', data['message'])
    
    def test_delete_repair_success(self):
        """测试删除报修记录成功"""
        # 创建报修记录
        with self.app.app_context():
            repair = RepairRecord(room_id=self.room_id, repair_type='网络', status=0)
            db.session.add(repair)
            db.session.commit()
            repair_id = repair.id
        
        response = self.client.delete(f'/api/repair/delete/{repair_id}',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        
        # 验证删除
        with self.app.app_context():
            repair = RepairRecord.query.get(repair_id)
            self.assertIsNone(repair)


class RepairModelTestCase(unittest.TestCase):
    """报修记录模型测试类"""
    
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
    
    def test_repair_record_creation(self):
        """测试报修记录创建"""
        with self.app.app_context():
            repair = RepairRecord(
                room_id=self.room_id,
                student_id=self.student_id,
                repair_type='家具',
                description='椅子坏了',
                contact_phone='13800138001',
                status=0
            )
            db.session.add(repair)
            db.session.commit()
            
            self.assertIsNotNone(repair.id)
            self.assertEqual(repair.repair_type, '家具')
            self.assertEqual(repair.status, 0)
    
    def test_repair_record_to_dict(self):
        """测试报修记录模型转字典"""
        with self.app.app_context():
            repair = RepairRecord(
                room_id=self.room_id,
                student_id=self.student_id,
                repair_type='水电',
                description='灯不亮',
                status=1
            )
            db.session.add(repair)
            db.session.commit()
            
            repair_dict = repair.to_dict()
            self.assertEqual(repair_dict['repair_type'], '水电')
            self.assertEqual(repair_dict['status'], 1)
            self.assertIn('room_number', repair_dict)
            self.assertIn('student_name', repair_dict)


def run_tests():
    """运行测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(RepairTestCase))
    suite.addTests(loader.loadTestsFromTestCase(RepairModelTestCase))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
