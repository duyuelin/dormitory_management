"""
房间管理模块测试代码
@author 结对小组 - 后端测试
@cross-testing duyuelin 交叉测试验证通过 (2026-05-21)
"""
import unittest
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User, Building, Room


class RoomTestCase(unittest.TestCase):
    """房间管理模块测试类"""
    
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
            
            # 创建测试宿舍楼
            building = Building(name='1号楼', code='B001', total_beds=0, available_beds=0)
            db.session.add(building)
            db.session.commit()
            
            # 创建测试房间
            room = Room(
                building_id=1,
                room_number='101',
                floor=1,
                total_beds=4,
                available_beds=4,
                room_type='四人间',
                price=1200,
                status=1
            )
            db.session.add(room)
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
    
    def test_get_room_list(self):
        """测试获取房间列表"""
        response = self.client.get('/api/room/list',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['room_number'], '101')
    
    def test_get_room_list_with_filter(self):
        """测试带筛选条件的房间列表"""
        # 添加另一个房间
        with self.app.app_context():
            room = Room(building_id=1, room_number='102', floor=1, total_beds=4, available_beds=0, status=2)
            db.session.add(room)
            db.session.commit()
        
        # 按状态筛选
        response = self.client.get('/api/room/list?status=2',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['room_number'], '102')
    
    def test_get_room_detail(self):
        """测试获取房间详情"""
        response = self.client.get('/api/room/1',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['data']['room_number'], '101')
    
    def test_get_available_rooms(self):
        """测试获取可入住房间"""
        response = self.client.get('/api/room/available',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        self.assertEqual(len(data['data']), 1)
    
    def test_add_room_success(self):
        """测试添加房间成功"""
        response = self.client.post('/api/room/add',
            data=json.dumps({
                'building_id': 1,
                'room_number': '201',
                'floor': 2,
                'total_beds': 6,
                'room_type': '六人间',
                'price': 1000
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['message'], '添加成功')
        
        # 验证宿舍楼床位统计更新
        with self.app.app_context():
            building = Building.query.get(1)
            self.assertEqual(building.total_beds, 6)
            self.assertEqual(building.available_beds, 6)
    
    def test_add_room_without_required_fields(self):
        """测试添加房间缺少必填字段"""
        response = self.client.post('/api/room/add',
            data=json.dumps({'room_number': '301'}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 500)
        self.assertIn('不能为空', data['message'])
    
    def test_update_room_success(self):
        """测试更新房间成功"""
        response = self.client.put('/api/room/update',
            data=json.dumps({
                'id': 1,
                'room_number': '101（已修改）',
                'room_type': '双人间',
                'price': 2000
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        
        # 验证更新
        with self.app.app_context():
            room = Room.query.get(1)
            self.assertEqual(room.room_type, '双人间')
            self.assertEqual(float(room.price), 2000)
    
    def test_delete_room_success(self):
        """测试删除房间成功"""
        # 添加一个要删除的房间
        with self.app.app_context():
            room = Room(building_id=1, room_number='999', total_beds=4, available_beds=4)
            db.session.add(room)
            db.session.commit()
            delete_id = room.id
        
        response = self.client.delete(f'/api/room/delete/{delete_id}',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        
        # 验证删除
        with self.app.app_context():
            room = Room.query.get(delete_id)
            self.assertIsNone(room)


class RoomModelTestCase(unittest.TestCase):
    """房间模型测试类"""
    
    def setUp(self):
        self.app = create_app('testing')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with self.app.app_context():
            db.create_all()
            # 创建宿舍楼
            building = Building(name='1号楼', code='B001')
            db.session.add(building)
            db.session.commit()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_room_creation(self):
        """测试房间创建"""
        with self.app.app_context():
            room = Room(
                building_id=1,
                room_number='101',
                floor=1,
                total_beds=4,
                available_beds=4
            )
            db.session.add(room)
            db.session.commit()
            
            self.assertIsNotNone(room.id)
            self.assertEqual(room.room_number, '101')
    
    def test_room_to_dict(self):
        """测试房间模型转字典"""
        with self.app.app_context():
            room = Room(
                building_id=1,
                room_number='101',
                total_beds=4,
                available_beds=4,
                price=1200
            )
            db.session.add(room)
            db.session.commit()
            
            room_dict = room.to_dict()
            self.assertEqual(room_dict['room_number'], '101')
            self.assertEqual(room_dict['total_beds'], 4)
            self.assertEqual(room_dict['price'], 1200)


def run_tests():
    """运行测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(RoomTestCase))
    suite.addTests(loader.loadTestsFromTestCase(RoomModelTestCase))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
