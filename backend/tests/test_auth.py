"""
用户认证模块测试代码
@author 结对小组 - 后端测试
@cross-testing han909 交叉测试验证通过 (2026-05-21)
"""
import unittest
import json
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User


class AuthTestCase(unittest.TestCase):
    """用户认证模块测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.app = create_app('testing')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            # 创建测试用户
            user = User(username='testuser', real_name='测试用户', role=1)
            user.set_password('test123')
            db.session.add(user)
            db.session.commit()
    
    def tearDown(self):
        """测试后清理"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_register_success(self):
        """测试用户注册成功"""
        response = self.client.post('/api/user/register',
            data=json.dumps({
                'username': 'newuser',
                'password': 'newpass123',
                'real_name': '新用户'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['message'], '注册成功')
    
    def test_register_duplicate_username(self):
        """测试重复用户名注册失败"""
        response = self.client.post('/api/user/register',
            data=json.dumps({
                'username': 'testuser',
                'password': 'test123'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 500)
        self.assertIn('用户名已存在', data['message'])
    
    def test_register_missing_fields(self):
        """测试缺少必填字段"""
        response = self.client.post('/api/user/register',
            data=json.dumps({'username': 'user'}),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 500)
        self.assertIn('不能为空', data['message'])
    
    def test_login_success(self):
        """测试用户登录成功"""
        response = self.client.post('/api/user/login',
            data=json.dumps({
                'username': 'testuser',
                'password': 'test123'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 200)
        self.assertIn('token', data['data'])
        self.assertIn('user', data['data'])
    
    def test_login_wrong_password(self):
        """测试密码错误"""
        response = self.client.post('/api/user/login',
            data=json.dumps({
                'username': 'testuser',
                'password': 'wrongpass'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 500)
        self.assertIn('用户名或密码错误', data['message'])
    
    def test_login_nonexistent_user(self):
        """测试用户不存在"""
        response = self.client.post('/api/user/login',
            data=json.dumps({
                'username': 'nonexistent',
                'password': 'test123'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 500)
        self.assertIn('用户名或密码错误', data['message'])
    
    def test_login_disabled_user(self):
        """测试禁用用户登录"""
        with self.app.app_context():
            user = User.query.filter_by(username='testuser').first()
            user.status = 0
            db.session.commit()
        
        response = self.client.post('/api/user/login',
            data=json.dumps({
                'username': 'testuser',
                'password': 'test123'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 500)
        self.assertIn('用户已被禁用', data['message'])
    
    def test_get_user_info_with_token(self):
        """测试使用Token获取用户信息"""
        # 先登录获取token
        login_response = self.client.post('/api/user/login',
            data=json.dumps({
                'username': 'testuser',
                'password': 'test123'
            }),
            content_type='application/json'
        )
        token = json.loads(login_response.data)['data']['token']
        
        # 使用token获取用户信息
        response = self.client.get('/api/user/info',
            headers={'Authorization': f'Bearer {token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['data']['username'], 'testuser')
    
    def test_get_user_info_without_token(self):
        """测试无Token访问用户信息"""
        response = self.client.get('/api/user/info')
        self.assertEqual(response.status_code, 401)


class AuthModelTestCase(unittest.TestCase):
    """用户模型测试类"""
    
    def setUp(self):
        self.app = create_app('testing')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_password_hashing(self):
        """测试密码加密"""
        with self.app.app_context():
            user = User(username='test')
            user.set_password('password123')
            self.assertTrue(user.check_password('password123'))
            self.assertFalse(user.check_password('wrongpassword'))
    
    def test_to_dict(self):
        """测试模型转字典"""
        with self.app.app_context():
            user = User(username='test', real_name='测试', role=1, status=1)
            user.set_password('pass')
            db.session.add(user)
            db.session.commit()
            
            user_dict = user.to_dict()
            self.assertEqual(user_dict['username'], 'test')
            self.assertEqual(user_dict['real_name'], '测试')
            self.assertEqual(user_dict['role'], 1)
            self.assertNotIn('password_hash', user_dict)


def run_tests():
    """运行测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(AuthTestCase))
    suite.addTests(loader.loadTestsFromTestCase(AuthModelTestCase))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
