"""
宿舍楼管理模块测试代码
@author 结对小组 - 后端测试
@cross-testing han909 交叉测试验证通过 (2026-05-21)
"""
import unittest
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User, Building, Room


class BuildingTestCase(unittest.TestCase):
    """宿舍楼管理模块测试类"""
    
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
            building = Building(
                name='1号楼',
                code='B001',
                floors=6,
                rooms_per_floor=20,
                total_beds=480,
                available_beds=480,
                manager='张宿管',
                manager_phone='13800138001',
                gender='男',
                status=1
            )
            db.session.add(building)
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
    
    def test_get_building_list(self):
        """测试获取宿舍楼列表"""
        response = self.client.get('/api/building/list',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['name'], '1号楼')
    
    def test_get_building_detail(self):
        """测试获取宿舍楼详情"""
        response = self.client.get('/api/building/1',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['data']['name'], '1号楼')
    
    def test_get_nonexistent_building(self):
        """测试获取不存在的宿舍楼"""
        response = self.client.get('/api/building/999',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 500)
        self.assertIn('不存在', data['message'])
    
    def test_add_building_success(self):
        """测试添加宿舍楼成功"""
        response = self.client.post('/api/building/add',
            data=json.dumps({
                'name': '2号楼',
                'code': 'B002',
                'floors': 5,
                'rooms_per_floor': 15,
                'manager': '李宿管',
                'gender': '女'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['message'], '添加成功')
        
        # 验证是否添加成功
        with self.app.app_context():
            building = Building.query.filter_by(code='B002').first()
            self.assertIsNotNone(building)
            self.assertEqual(building.name, '2号楼')
    
    def test_add_building_without_name(self):
        """测试添加宿舍楼缺少名称"""
        response = self.client.post('/api/building/add',
            data=json.dumps({'code': 'B003'}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 500)
        self.assertIn('楼名不能为空', data['message'])
    
    def test_update_building_success(self):
        """测试更新宿舍楼成功"""
        response = self.client.put('/api/building/update',
            data=json.dumps({
                'id': 1,
                'name': '1号楼（已修改）',
                'manager': '王宿管'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        
        # 验证更新
        with self.app.app_context():
            building = Building.query.get(1)
            self.assertEqual(building.name, '1号楼（已修改）')
            self.assertEqual(building.manager, '王宿管')
    
    def test_update_nonexistent_building(self):
        """测试更新不存在的宿舍楼"""
        response = self.client.put('/api/building/update',
            data=json.dumps({'id': 999, 'name': '测试'}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 500)
        self.assertIn('不存在', data['message'])
    
    def test_delete_building_success(self):
        """测试删除宿舍楼成功"""
        # 先添加一个要删除的宿舍楼
        with self.app.app_context():
            building = Building(name='待删除楼', code='B999')
            db.session.add(building)
            db.session.commit()
            delete_id = building.id
        
        response = self.client.delete(f'/api/building/delete/{delete_id}',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        
        # 验证删除
        with self.app.app_context():
            building = Building.query.get(delete_id)
            self.assertIsNone(building)
    
    def test_get_building_rooms(self):
        """测试获取宿舍楼的房间列表"""
        # 先添加房间
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
        
        response = self.client.get('/api/building/1/rooms',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['room_number'], '101')


class BuildingModelTestCase(unittest.TestCase):
    """宿舍楼模型测试类"""
    
    def setUp(self):
        self.app = create_app('testing')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_building_creation(self):
        """测试宿舍楼创建"""
        with self.app.app_context():
            building = Building(
                name='测试楼',
                code='T001',
                floors=6,
                total_beds=240,
                available_beds=240
            )
            db.session.add(building)
            db.session.commit()
            
            self.assertIsNotNone(building.id)
            self.assertEqual(building.name, '测试楼')
    
    def test_building_to_dict(self):
        """测试宿舍楼模型转字典"""
        with self.app.app_context():
            building = Building(name='测试楼', code='T001')
            db.session.add(building)
            db.session.commit()
            
            building_dict = building.to_dict()
            self.assertEqual(building_dict['name'], '测试楼')
            self.assertEqual(building_dict['code'], 'T001')
            self.assertIn('create_time', building_dict)


def run_tests():
    """运行测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(BuildingTestCase))
    suite.addTests(loader.loadTestsFromTestCase(BuildingModelTestCase))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
