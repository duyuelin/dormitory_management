"""
后端测试运行器 - 运行所有模块测试
@author 结对小组 - 后端测试

使用方法:
    python run_all_tests.py              # 运行所有测试
    python run_all_tests.py auth         # 运行用户认证模块测试
    python run_all_tests.py building     # 运行宿舍楼管理模块测试
    python run_all_tests.py room         # 运行房间管理模块测试
    python run_all_tests.py student      # 运行学生管理模块测试
    python run_all_tests.py checkin      # 运行入住管理模块测试
    python run_all_tests.py repair       # 运行报修管理模块测试
"""
import unittest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入所有测试模块
from tests.test_auth import AuthTestCase, AuthModelTestCase
from tests.test_building import BuildingTestCase, BuildingModelTestCase
from tests.test_room import RoomTestCase, RoomModelTestCase
from tests.test_student import StudentTestCase, StudentModelTestCase
from tests.test_checkin import CheckInTestCase, CheckInModelTestCase
from tests.test_repair import RepairTestCase, RepairModelTestCase


def run_all_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    test_classes = [
        AuthTestCase, AuthModelTestCase,
        BuildingTestCase, BuildingModelTestCase,
        RoomTestCase, RoomModelTestCase,
        StudentTestCase, StudentModelTestCase,
        CheckInTestCase, CheckInModelTestCase,
        RepairTestCase, RepairModelTestCase
    ]
    
    for test_class in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(test_class))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


def run_module_tests(module_name):
    """运行指定模块的测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    module_map = {
        'auth': (AuthTestCase, AuthModelTestCase),
        'building': (BuildingTestCase, BuildingModelTestCase),
        'room': (RoomTestCase, RoomModelTestCase),
        'student': (StudentTestCase, StudentModelTestCase),
        'checkin': (CheckInTestCase, CheckInModelTestCase),
        'repair': (RepairTestCase, RepairModelTestCase)
    }
    
    if module_name not in module_map:
        print(f"错误: 未知模块 '{module_name}'")
        print(f"可用模块: {', '.join(module_map.keys())}")
        return False
    
    for test_class in module_map[module_name]:
        suite.addTests(loader.loadTestsFromTestCase(test_class))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        module = sys.argv[1]
        success = run_module_tests(module)
    else:
        print("=" * 60)
        print("  宿舍管理系统后端测试")
        print("=" * 60)
        success = run_all_tests()
    
    sys.exit(0 if success else 1)
