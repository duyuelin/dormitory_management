# 宿舍管理系统

> 人人结对编程作业 - 宿舍管理系统（Python Flask + Vue3）

## 基本信息

| 学号 | 姓名 | 技术侧重点 |
|------|------|-----------|
| 20240010001 | 张三 | 后端Python Flask |
| 20240010002 | 李四 | 前端Vue3 |

**项目地址**: https://github.com/your-team/dormitory-system

---

## 技术栈声明

- **后端**: Python 3.10+ + Flask 3.0 + Flask-SQLAlchemy + Flask-JWT-Extended + MySQL 8.0
- **前端**: Vue 3 + Element Plus + Vite + Axios

---

## 功能模块

1. **用户模块**: 用户登录、JWT认证
2. **宿舍楼管理**: 宿舍楼CRUD、床位统计
3. **房间管理**: 房间CRUD、床位管理
4. **学生管理**: 学生信息CRUD
5. **入住管理**: 入住办理、退宿办理
6. **报修管理**: 报修提交、报修处理

---

## 本地部署步骤

### 1. 环境要求

- Python 3.10+
- Node.js 18+
- MySQL 8.0+

### 2. 数据库初始化

```sql
CREATE DATABASE dormitory_system DEFAULT CHARACTER SET utf8mb4;
```

### 3. 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 修改数据库配置（config.py中的用户名密码）

# 初始化数据库
python init_db.py

# 启动服务
python run.py
# 访问 http://localhost:5000
```

### 4. 前端启动

```bash
cd frontend
npm install
npm run dev
# 访问 http://localhost:5173
```

---

## 测试账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |
| 普通管理员 | zhangsan | 123456 |

---

## 项目结构

```
dormitory-system/
├── backend/              # Python Flask后端
│   ├── models/          # SQLAlchemy模型
│   ├── routes/          # API路由
│   ├── utils/           # 工具类
│   ├── app.py           # 应用主程序
│   ├── config.py        # 配置文件
│   ├── init_db.py       # 数据库初始化
│   └── requirements.txt # Python依赖
├── frontend/            # Vue3前端
│   ├── src/views/       # 页面
│   ├── src/api/         # API接口
│   └── package.json
└── doc/                 # 文档
```

---

## API接口

### 用户接口
| 接口 | 方法 | 描述 |
|------|------|------|
| /api/user/login | POST | 用户登录 |
| /api/user/register | POST | 用户注册 |

### 宿舍楼接口
| 接口 | 方法 | 描述 |
|------|------|------|
| /api/building/list | GET | 宿舍楼列表 |
| /api/building/add | POST | 添加宿舍楼 |
| /api/building/update | PUT | 更新宿舍楼 |
| /api/building/delete/<id> | DELETE | 删除宿舍楼 |

### 房间接口
| 接口 | 方法 | 描述 |
|------|------|------|
| /api/room/list | GET | 房间列表 |
| /api/room/available | GET | 可入住房间 |
| /api/room/add | POST | 添加房间 |

### 学生接口
| 接口 | 方法 | 描述 |
|------|------|------|
| /api/student/list | GET | 学生列表 |
| /api/student/add | POST | 添加学生 |

### 入住接口
| 接口 | 方法 | 描述 |
|------|------|------|
| /api/checkin/list | GET | 入住记录列表 |
| /api/checkin/check-in | POST | 办理入住 |
| /api/checkin/check-out/<id> | POST | 办理退宿 |

### 报修接口
| 接口 | 方法 | 描述 |
|------|------|------|
| /api/repair/list | GET | 报修记录列表 |
| /api/repair/submit | POST | 提交报修 |
| /api/repair/handle/<id> | POST | 处理报修 |
