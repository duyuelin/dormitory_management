"""
集成测试 - 跨模块端到端测试
@author 结对小组 - 交叉测试第1轮
@test-author han909
"""
import unittest
import json
import sys
import os
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User, Building, Room, Student, CheckInRecord, RepairRecord


class IntegrationTestCase(unittest.TestCase):
    """跨模块集成测试 — 第1轮：han909编写"""

    def setUp(self):
        self.app = create_app('testing')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            admin = User(username='admin', real_name='管理员', role=1)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

        self.admin_token = self._get_token('admin', 'admin123')

    def _get_token(self, username, password):
        resp = self.client.post('/api/user/login',
            data=json.dumps({'username': username, 'password': password}),
            content_type='application/json')
        return json.loads(resp.data)['data']['token']

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # ========== 测试1：完整入住流程 ==========
    def test_full_checkin_workflow(self):
        """集成测试：创建楼→创建房间→添加学生→办理入住→验证全链路状态"""
        headers = {'Authorization': f'Bearer {self.admin_token}'}

        # Step 1: 创建宿舍楼
        resp = self.client.post('/api/building/add',
            data=json.dumps({'name': '1号楼', 'code': 'B001', 'floors': 6, 'gender': '男'}),
            content_type='application/json', headers=headers)
        self.assertEqual(json.loads(resp.data)['code'], 200)

        # Step 2: 在楼下创建房间
        resp = self.client.post('/api/room/add',
            data=json.dumps({'building_id': 1, 'room_number': '101', 'floor': 1,
                             'total_beds': 4, 'room_type': '四人间', 'price': 1200}),
            content_type='application/json', headers=headers)
        self.assertEqual(json.loads(resp.data)['code'], 200)

        # Step 3: 添加学生
        resp = self.client.post('/api/student/add',
            data=json.dumps({'student_id': '2024001001', 'name': '张三',
                             'gender': '男', 'college': '计算机学院'}),
            content_type='application/json', headers=headers)
        self.assertEqual(json.loads(resp.data)['code'], 200)

        # Step 4: 办理入住
        resp = self.client.post('/api/checkin/check-in',
            data=json.dumps({'student_id': 1, 'room_id': 1, 'bed_number': 1}),
            content_type='application/json', headers=headers)
        self.assertEqual(json.loads(resp.data)['code'], 200)

        # Step 5: 验证全链路状态
        with self.app.app_context():
            building = Building.query.get(1)
            room = Room.query.get(1)
            student = Student.query.get(1)

            self.assertEqual(building.available_beds, 3)   # 4-1
            self.assertEqual(room.available_beds, 3)       # 4-1
            self.assertEqual(student.status, 1)            # 在住

    # ========== 测试2：完整退宿流程 ==========
    def test_full_checkout_workflow(self):
        """集成测试：入住→退宿→验证状态恢复"""
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        with self.app.app_context():
            b = Building(name='1号楼', code='B001', total_beds=4, available_beds=4)
            r = Room(building_id=1, room_number='101', total_beds=4, available_beds=4)
            s = Student(student_id='2024001001', name='张三', status=2)
            db.session.add_all([b, r, s])
            db.session.commit()

        # 入住
        resp = self.client.post('/api/checkin/check-in',
            data=json.dumps({'student_id': 1, 'room_id': 1, 'bed_number': 1}),
            content_type='application/json', headers=headers)
        self.assertEqual(json.loads(resp.data)['code'], 200)

        # 获取入住记录ID
        with self.app.app_context():
            record = CheckInRecord.query.first()

        # 退宿
        resp = self.client.post(f'/api/checkin/check-out/{record.id}',
            headers=headers)
        self.assertEqual(json.loads(resp.data)['code'], 200)

        # 验证状态恢复
        with self.app.app_context():
            room = Room.query.get(1)
            student = Student.query.get(1)
            self.assertEqual(room.available_beds, 4)   # 恢复
            self.assertEqual(student.status, 0)         # 退宿

    # ========== 测试3：删除有房间的宿舍楼（边界条件） ==========
    def test_delete_building_with_rooms(self):
        """集成测试：删除包含房间的宿舍楼，预期返回错误"""
        headers = {'Authorization': f'Bearer {self.admin_token}'}

        # 创建楼和房间
        with self.app.app_context():
            b = Building(name='1号楼', code='B001')
            db.session.add(b)
            db.session.flush()
            r = Room(building_id=b.id, room_number='101', total_beds=4, available_beds=4)
            db.session.add(r)
            db.session.commit()
            building_id = b.id

        # 尝试删除有房间的楼
        resp = self.client.delete(f'/api/building/delete/{building_id}', headers=headers)
        data = json.loads(resp.data)
        # 应该返回错误，因为还有关联房间
        self.assertNotEqual(data['code'], 200)

    # ========== 测试4：报修闭环流程 ==========
    def test_repair_lifecycle(self):
        """集成测试：创建房间→提交报修→处理报修→验证完成"""
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        with self.app.app_context():
            b = Building(name='1号楼', code='B001')
            db.session.add(b)
            db.session.flush()
            r = Room(building_id=b.id, room_number='101', total_beds=4, available_beds=4)
            db.session.add(r)
            db.session.commit()
            room_id = r.id

        # 提交报修
        resp = self.client.post('/api/repair/submit',
            data=json.dumps({'room_id': room_id, 'repair_type': '水电',
                             'description': '水龙头漏水', 'contact_phone': '13800001111'}),
            content_type='application/json', headers=headers)
        self.assertEqual(json.loads(resp.data)['code'], 200)

        # 处理报修
        with self.app.app_context():
            repair = RepairRecord.query.first()
        resp = self.client.post(f'/api/repair/handle/{repair.id}',
            data=json.dumps({'status': 2, 'handle_result': '已更换水龙头'}),
            content_type='application/json', headers=headers)
        self.assertEqual(json.loads(resp.data)['code'], 200)

        # 验证
        with self.app.app_context():
            repair = RepairRecord.query.first()
            self.assertEqual(repair.status, 2)
            self.assertEqual(repair.handle_result, '已更换水龙头')
            self.assertIsNotNone(repair.handle_time)
            self.assertEqual(repair.handler, '管理员')

    # ========== 测试5：学生状态流转 ==========
    def test_student_status_transitions(self):
        """集成测试：待入住→在住→退宿 状态正确流转"""
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        with self.app.app_context():
            b = Building(name='1号楼', code='B001', total_beds=4, available_beds=4)
            r = Room(building_id=1, room_number='101', total_beds=4, available_beds=4)
            s = Student(student_id='2024001001', name='张三', status=2)
            db.session.add_all([b, r, s])
            db.session.commit()

        # 状态2: 待入住
        with self.app.app_context():
            self.assertEqual(Student.query.get(1).status, 2)

        # 入住 → 状态1: 在住
        resp = self.client.post('/api/checkin/check-in',
            data=json.dumps({'student_id': 1, 'room_id': 1, 'bed_number': 1}),
            content_type='application/json', headers=headers)
        self.assertEqual(json.loads(resp.data)['code'], 200)

        # 退宿 → 状态0: 退宿
        with self.app.app_context():
            record = CheckInRecord.query.first()
        resp = self.client.post(f'/api/checkin/check-out/{record.id}', headers=headers)
        self.assertEqual(json.loads(resp.data)['code'], 200)

        with self.app.app_context():
            self.assertEqual(Student.query.get(1).status, 0)


    # ====== 第2轮：duyuelin编写 ======

    def test_checkin_bed_exceeds_capacity(self):
        """边界测试：办理入住时床位号超过房间总床位数，应拒绝"""
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        with self.app.app_context():
            b = Building(name='1号楼', code='B001', total_beds=4, available_beds=4)
            r = Room(building_id=1, room_number='101', total_beds=4, available_beds=4)
            s = Student(student_id='2024001001', name='张三', status=2)
            db.session.add_all([b, r, s])
            db.session.commit()

        # 尝试入住床位5（房间只有4张床）
        resp = self.client.post('/api/checkin/check-in',
            data=json.dumps({'student_id': 1, 'room_id': 1, 'bed_number': 5}),
            content_type='application/json', headers=headers)
        data = json.loads(resp.data)
        self.assertNotEqual(data['code'], 200)

    def test_concurrent_checkins_fill_room(self):
        """边界测试：连续入住直到房间满，验证房间状态变为已满"""
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        with self.app.app_context():
            b = Building(name='1号楼', code='B001', total_beds=2, available_beds=2)
            r = Room(building_id=1, room_number='101', total_beds=2, available_beds=2)
            s1 = Student(student_id='2024001001', name='张三', status=2)
            s2 = Student(student_id='2024001002', name='李四', status=2)
            db.session.add_all([b, r, s1, s2])
            db.session.commit()

        # 第一人入住
        resp = self.client.post('/api/checkin/check-in',
            data=json.dumps({'student_id': 1, 'room_id': 1, 'bed_number': 1}),
            content_type='application/json', headers=headers)
        self.assertEqual(json.loads(resp.data)['code'], 200)

        # 第二人入住
        resp = self.client.post('/api/checkin/check-in',
            data=json.dumps({'student_id': 2, 'room_id': 1, 'bed_number': 2}),
            content_type='application/json', headers=headers)
        self.assertEqual(json.loads(resp.data)['code'], 200)

        # 验证房间已满
        with self.app.app_context():
            room = Room.query.get(1)
            self.assertEqual(room.available_beds, 0)
            self.assertEqual(room.status, 2)

    def test_room_update_beds_propagate(self):
        """一致性测试：更新房间总床位后，宿舍楼床位统计同步更新"""
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        with self.app.app_context():
            b = Building(name='1号楼', code='B001', total_beds=4, available_beds=4)
            r = Room(building_id=1, room_number='101', total_beds=4, available_beds=4)
            db.session.add_all([b, r])
            db.session.commit()

        # 更新房间总床位从4改为6
        resp = self.client.put('/api/room/update',
            data=json.dumps({'id': 1, 'total_beds': 6, 'available_beds': 6}),
            content_type='application/json', headers=headers)
        self.assertEqual(json.loads(resp.data)['code'], 200)

        # 验证宿舍楼床位同步
        with self.app.app_context():
            building = Building.query.get(1)
            self.assertEqual(building.total_beds, 6)
            self.assertEqual(building.available_beds, 6)

    def test_checkout_then_new_checkin(self):
        """流程测试：退宿后释放床位，另一学生入住同一床位"""
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        with self.app.app_context():
            b = Building(name='1号楼', code='B001', total_beds=4, available_beds=4)
            r = Room(building_id=1, room_number='101', total_beds=4, available_beds=4)
            s1 = Student(student_id='2024001001', name='张三', status=2)
            s2 = Student(student_id='2024001002', name='李四', status=2)
            db.session.add_all([b, r, s1, s2])
            db.session.commit()

        # 张三入住床位1
        resp = self.client.post('/api/checkin/check-in',
            data=json.dumps({'student_id': 1, 'room_id': 1, 'bed_number': 1}),
            content_type='application/json', headers=headers)
        self.assertEqual(json.loads(resp.data)['code'], 200)

        # 获取入住记录
        with self.app.app_context():
            record = CheckInRecord.query.first()

        # 张三退宿
        resp = self.client.post(f'/api/checkin/check-out/{record.id}', headers=headers)
        self.assertEqual(json.loads(resp.data)['code'], 200)

        # 李四入住同一床位
        resp = self.client.post('/api/checkin/check-in',
            data=json.dumps({'student_id': 2, 'room_id': 1, 'bed_number': 1}),
            content_type='application/json', headers=headers)
        self.assertEqual(json.loads(resp.data)['code'], 200)

        # 验证李四在住，房间床位正确
        with self.app.app_context():
            s2 = Student.query.get(2)
            self.assertEqual(s2.status, 1)
            room = Room.query.get(1)
            self.assertEqual(room.available_beds, 3)

    def test_delete_room_with_active_checkin(self):
        """边界测试：删除有在住记录的宿舍楼时应拒绝（防止孤儿记录）"""
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        with self.app.app_context():
            b = Building(name='1号楼', code='B001', total_beds=4, available_beds=4)
            r = Room(building_id=1, room_number='101', total_beds=4, available_beds=4)
            s = Student(student_id='2024001001', name='张三', status=2)
            db.session.add_all([b, r, s])
            db.session.commit()
            room_id = r.id

        # 入住
        resp = self.client.post('/api/checkin/check-in',
            data=json.dumps({'student_id': 1, 'room_id': 1, 'bed_number': 1}),
            content_type='application/json', headers=headers)
        self.assertEqual(json.loads(resp.data)['code'], 200)

        # 尝试删除有在住记录的房间
        resp = self.client.delete(f'/api/room/delete/{room_id}', headers=headers)
        data = json.loads(resp.data)
        self.assertNotEqual(data['code'], 200)


def run_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(IntegrationTestCase))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
