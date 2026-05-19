"""
宿舍管理系统 - Flask后端主程序
@author 结对小组
"""
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config
from models import db
from routes.auth import auth_bp
from routes.building import building_bp

def create_app(config_name='default'):
    """应用工厂函数"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    db.init_app(app)
    JWTManager(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # 注册蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(building_bp)
    
    # 根路由
    @app.route('/')
    def index():
        return {
            'message': '宿舍管理系统API',
            'version': '1.0.0',
            'modules': ['用户管理', '宿舍楼管理', '房间管理', '学生管理', '入住管理', '报修管理']
        }
    
    # 错误处理
    @app.errorhandler(404)
    def not_found(error):
        return {'code': 404, 'message': '接口不存在', 'data': None}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'code': 500, 'message': '服务器内部错误', 'data': None}, 500
    
    return app

# 创建应用实例
app = create_app('development')

if __name__ == '__main__':
    print("=" * 50)
    print("  宿舍管理系统后端启动成功！")
    print("  API地址: http://localhost:5000")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
# backend/app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # 在这里创建 db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)  # 初始化 db
    
    with app.app_context():
        from models import User  # 在这里导入 models
    
    return app