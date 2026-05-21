"""
学生管理模块测试代码
@author 结对小组 - 后端测试
@cross-testing han909 交叉测试验证通过 (2026-05-21)
"""
import unittest
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User, Student


class StudentTestCase(unittest.TestCase):
    """学生管理模块测试类"""
    
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
            
            # 创建测试学生
            student = Student(
                student_id='2024001001',
                name='张三',
                gender='男',
                phone='13800138001',
                email='zhangsan@example.com',
                college='计算机学院',
                major='软件工程',
                class_name='软件2401',
                grade='2024',
                status=2  # 待入住
            )
            db.session.add(student)
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
    
    def test_get_student_list(self):
        """测试获取学生列表"""
        response = self.client.get('/api/student/list',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['name'], '张三')
    
    def test_get_student_list_with_keyword(self):
        """测试按关键词搜索学生"""
        # 添加另一个学生
        with self.app.app_context():
            student = Student(student_id='2024001002', name='李四', status=2)
            db.session.add(student)
            db.session.commit()
        
        response = self.client.get('/api/student/list?keyword=张三',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['name'], '张三')
    
    def test_get_student_list_with_status(self):
        """测试按状态筛选学生"""
        # 添加不同状态的学生
        with self.app.app_context():
            student = Student(student_id='2024001002', name='李四', status=1)
            db.session.add(student)
            db.session.commit()
        
        response = self.client.get('/api/student/list?status=1',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['name'], '李四')
    
    def test_get_student_detail(self):
        """测试获取学生详情"""
        response = self.client.get('/api/student/1',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['data']['name'], '张三')
        self.assertEqual(data['data']['student_id'], '2024001001')
    
    def test_add_student_success(self):
        """测试添加学生成功"""
        response = self.client.post('/api/student/add',
            data=json.dumps({
                'student_id': '2024001002',
                'name': '李四',
                'gender': '女',
                'phone': '13800138002',
                'college': '电子学院',
                'major': '电子信息',
                'class_name': '电信2401',
                'grade': '2024'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['message'], '添加成功')
        
        # 验证学生状态为待入住
        with self.app.app_context():
            student = Student.query.filter_by(student_id='2024001002').first()
            self.assertEqual(student.status, 2)
    
    def test_add_student_duplicate_id(self):
        """测试添加重复学号的学生"""
        response = self.client.post('/api/student/add',
            data=json.dumps({
                'student_id': '2024001001',
                'name': '重复学生'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 500)
        self.assertIn('学号已存在', data['message'])
    
    def test_add_student_without_required_fields(self):
        """测试添加学生缺少必填字段"""
        response = self.client.post('/api/student/add',
            data=json.dumps({'name': '测试'}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 500)
        self.assertIn('不能为空', data['message'])
    
    def test_update_student_success(self):
        """测试更新学生成功"""
        response = self.client.put('/api/student/update',
            data=json.dumps({
                'id': 1,
                'name': '张三（已修改）',
                'phone': '13900139001',
                'college': '人工智能学院'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        
        # 验证更新
        with self.app.app_context():
            student = Student.query.get(1)
            self.assertEqual(student.name, '张三（已修改）')
            self.assertEqual(student.college, '人工智能学院')
    
    def test_delete_student_success(self):
        """测试删除学生成功"""
        # 添加一个要删除的学生
        with self.app.app_context():
            student = Student(student_id='2024999999', name='待删除')
            db.session.add(student)
            db.session.commit()
            delete_id = student.id
        
        response = self.client.delete(f'/api/student/delete/{delete_id}',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        
        # 验证删除
        with self.app.app_context():
            student = Student.query.get(delete_id)
            self.assertIsNone(student)


class StudentModelTestCase(unittest.TestCase):
    """学生模型测试类"""
    
    def setUp(self):
        self.app = create_app('testing')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_student_creation(self):
        """测试学生创建"""
        with self.app.app_context():
            student = Student(
                student_id='2024001001',
                name='张三',
                gender='男',
                status=2
            )
            db.session.add(student)
            db.session.commit()
            
            self.assertIsNotNone(student.id)
            self.assertEqual(student.name, '张三')
            self.assertEqual(student.status, 2)
    
    def test_student_to_dict(self):
        """测试学生模型转字典"""
        with self.app.app_context():
            student = Student(
                student_id='2024001001',
                name='张三',
                college='计算机学院',
                status=1
            )
            db.session.add(student)
            db.session.commit()
            
            student_dict = student.to_dict()
            self.assertEqual(student_dict['name'], '张三')
            self.assertEqual(student_dict['student_id'], '2024001001')
            self.assertEqual(student_dict['college'], '计算机学院')
            self.assertNotIn('id_card', student_dict)


def run_tests():
    """运行测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(StudentTestCase))
    suite.addTests(loader.loadTestsFromTestCase(StudentModelTestCase))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
