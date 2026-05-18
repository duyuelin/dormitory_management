"""
数据库初始化脚本
@author 结对小组
"""
from app import create_app
from models import db, User, Building, Room, Student, CheckInRecord, RepairRecord
from datetime import date, timedelta

def init_database():
    """初始化数据库"""
    app = create_app('development')
    
    with app.app_context():
        # 创建所有表
        db.create_all()
        print("✓ 数据库表创建完成")
        
        # 检查是否已有数据
        if User.query.first():
            print("✓ 数据库已有数据，跳过初始化")
            return
        
        # 创建管理员用户
        admin = User(
            username='admin',
            real_name='系统管理员',
            phone='13800138000',
            role=1,
            status=1
        )
        admin.set_password('admin123')
        
        # 创建普通管理员
        manager1 = User(
            username='zhangsan',
            real_name='张三',
            phone='13800138001',
            role=0,
            status=1
        )
        manager1.set_password('123456')
        
        manager2 = User(
            username='lisi',
            real_name='李四',
            phone='13800138002',
            role=0,
            status=1
        )
        manager2.set_password('123456')
        
        db.session.add_all([admin, manager1, manager2])
        db.session.commit()
        print("✓ 用户数据初始化完成")
        
        # 创建宿舍楼
        buildings = [
            Building(name='1号楼', code='B001', floors=6, rooms_per_floor=30, 
                    total_beds=720, available_beds=680, manager='王大爷', 
                    manager_phone='13900139001', gender='男'),
            Building(name='2号楼', code='B002', floors=6, rooms_per_floor=30,
                    total_beds=720, available_beds=650, manager='李阿姨',
                    manager_phone='13900139002', gender='女'),
            Building(name='3号楼', code='B003', floors=8, rooms_per_floor=25,
                    total_beds=800, available_beds=750, manager='赵大爷',
                    manager_phone='13900139003', gender='男'),
        ]
        db.session.add_all(buildings)
        db.session.commit()
        print("✓ 宿舍楼数据初始化完成")
        
        # 创建房间
        rooms = []
        for floor in range(1, 4):  # 1-3层
            for room_num in range(1, 6):  # 每层5个房间
                room_number = f"{floor}0{room_num}"
                rooms.append(Room(
                    building_id=1,
                    room_number=room_number,
                    floor=floor,
                    total_beds=4,
                    available_beds=4,
                    room_type='四人间',
                    price=1200,
                    status=1
                ))
        db.session.add_all(rooms)
        db.session.commit()
        print("✓ 房间数据初始化完成")
        
        # 创建学生
        students = [
            Student(student_id='2024001001', name='张明', gender='男', 
                   phone='15800001001', college='计算机学院', major='软件工程',
                   class_name='软工2401', grade='2024', status=2),
            Student(student_id='2024001002', name='李华', gender='男',
                   phone='15800001002', college='计算机学院', major='计算机科学',
                   class_name='计科2401', grade='2024', status=2),
            Student(student_id='2024001003', name='王芳', gender='女',
                   phone='15800001003', college='外国语学院', major='英语',
                   class_name='英语2401', grade='2024', status=1),
            Student(student_id='2024001004', name='赵强', gender='男',
                   phone='15800001004', college='机械学院', major='机械工程',
                   class_name='机械2401', grade='2024', status=2),
        ]
        db.session.add_all(students)
        db.session.commit()
        print("✓ 学生数据初始化完成")
        
        # 创建入住记录
        checkins = [
            CheckInRecord(student_id=3, room_id=1, bed_number=1,
                         check_in_date=date.today() - timedelta(days=30),
                         status=1),
        ]
        db.session.add_all(checkins)
        
        # 更新房间状态
        rooms[0].available_beds = 3
        
        db.session.commit()
        print("✓ 入住记录初始化完成")
        
        # 创建报修记录
        repairs = [
            RepairRecord(room_id=1, student_id=3, repair_type='水电',
                        description='卫生间水龙头漏水', contact_phone='15800001003',
                        status=0),
            RepairRecord(room_id=2, repair_type='家具',
                        description='椅子腿松动', contact_phone='15800001001',
                        status=1, handler='维修师傅老王'),
        ]
        db.session.add_all(repairs)
        db.session.commit()
        print("✓ 报修记录初始化完成")
        
        print("\n" + "=" * 50)
        print("数据库初始化完成！")
        print("测试账号：")
        print("  管理员：admin / admin123")
        print("  普通管理员：zhangsan / 123456")
        print("=" * 50)

if __name__ == '__main__':
    init_database()
