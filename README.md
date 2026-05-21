# 宿舍管理系统

> 人人结对编程作业 — 宿舍管理系统（Python Flask + Vue3 + Element Plus）

## 基本信息

| 学号 | 姓名 | 技术侧重点 |
|------|------|-----------|
| 233401010308 | duyuelin | 后端 Python Flask |
| 233401010306 | han909 | 前端 Vue3 |

**项目地址**: https://github.com/duyuelin/dormitory_management

---

## 技术栈

- **后端**: Python 3.10+ / Flask / Flask-SQLAlchemy / Flask-JWT-Extended / SQLite(测试) + MySQL(生产)
- **前端**: Vue 3 / Element Plus / Vite / Axios
- **协作**: Git Feature Branch Workflow / GitHub Pull Request / 交叉测试

---

## 功能模块

| 模块 | 后端 | 前端 | 测试 |
|------|------|------|------|
| 用户认证 | 登录/注册/JWT认证 | Login.vue | 11 项 |
| 宿舍楼管理 | 楼栋CRUD + 床位统计 | BuildingList.vue | 11 项 |
| 房间管理 | 房间CRUD + 可用房间查询 | RoomList.vue | 10 项 |
| 学生管理 | 学生CRUD + 关键词搜索 | StudentList.vue | 11 项 |
| 入住管理 | 入住/退宿 + 床位校验 | CheckInList.vue | 11 项 |
| 报修管理 | 报修提交/处理/删除 | RepairList.vue | 10 项 |
| **合计** | **6 个模块** | **6 个页面** | **64 项 + 10 项集成测试** |

---

## 开发过程

### Git 分支工作流

```
feature/xxx → develop → main
```

每个模块在独立 feature 分支开发，通过 Pull Request 合并到 develop，最终发布到 main。

### 交叉测试

| 轮次 | 测试编写 | 运行 & 修复 | 发现问题 |
|------|---------|------------|---------|
| 第1轮 | han909 | duyuelin | 入住/退宿时宿舍楼床位未同步更新 |
| 第2轮 | duyuelin | han909 | 床位号未校验是否超出房间容量 |

---

## 本地部署

### 1. 环境要求

- Python 3.10+
- Node.js 18+
- MySQL 8.0（可选，测试使用 SQLite 内存数据库）

### 2. 后端启动

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py
# 访问 http://localhost:5000
```

### 3. 前端启动

```bash
cd frontend
npm install
npm run dev
# 访问 http://localhost:5173
```

### 4. 运行测试

```bash
cd backend
python tests/test_auth.py
python tests/test_building.py
python tests/test_room.py
python tests/test_student.py
python tests/test_checkin.py
python tests/test_repair.py
python tests/test_integration.py
```

---

## 测试账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |

---

## 项目结构

```
dormitory_management/
├── backend/
│   ├── models/               # SQLAlchemy 模型
│   │   ├── user.py
│   │   ├── building.py
│   │   ├── room.py
│   │   ├── student.py
│   │   ├── checkin.py
│   │   └── repair.py
│   ├── routes/               # API 路由
│   │   ├── auth.py
│   │   ├── building.py
│   │   ├── room.py
│   │   ├── student.py
│   │   ├── checkin.py
│   │   └── repair.py
│   ├── utils/                # 工具类
│   │   ├── decorators.py     # 认证装饰器
│   │   └── response.py       # 统一响应格式
│   ├── tests/                # 测试代码
│   │   ├── test_auth.py      # 11 项
│   │   ├── test_building.py  # 11 项
│   │   ├── test_room.py      # 10 项
│   │   ├── test_student.py   # 11 项
│   │   ├── test_checkin.py   # 11 项
│   │   ├── test_repair.py    # 10 项
│   │   └── test_integration.py  # 10 项（交叉测试）
│   ├── app.py                # 应用主程序
│   ├── config.py             # 配置文件
│   └── requirements.txt
├── frontend/
│   ├── views/                # 页面组件
│   │   ├── Login.vue
│   │   ├── Layout.vue
│   │   ├── BuildingList.vue
│   │   ├── RoomList.vue
│   │   ├── StudentList.vue
│   │   ├── CheckInList.vue
│   │   └── RepairList.vue
│   ├── api/                  # API 调用
│   │   ├── user.js
│   │   ├── building.js
│   │   ├── room.js
│   │   ├── student.js
│   │   ├── checkin.js
│   │   └── repair.js
│   ├── router/               # 路由配置
│   │   └── index.js
│   ├── main.js
│   ├── App.vue
│   └── package.json
└── README.md
```

---

## API 接口

### 用户认证
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/user/register | 用户注册 |
| POST | /api/user/login | 用户登录 |
| GET | /api/user/info | 获取当前用户信息 |

### 宿舍楼管理
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/building/list | 宿舍楼列表 |
| GET | /api/building/&lt;id&gt; | 宿舍楼详情 |
| POST | /api/building/add | 添加宿舍楼 |
| PUT | /api/building/update | 更新宿舍楼 |
| DELETE | /api/building/delete/&lt;id&gt; | 删除宿舍楼 |
| GET | /api/building/&lt;id&gt;/rooms | 宿舍楼房间列表 |

### 房间管理
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/room/list | 房间列表（支持status筛选） |
| GET | /api/room/available | 可入住房间 |
| GET | /api/room/&lt;id&gt; | 房间详情 |
| POST | /api/room/add | 添加房间 |
| PUT | /api/room/update | 更新房间 |
| DELETE | /api/room/delete/&lt;id&gt; | 删除房间 |

### 学生管理
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/student/list | 学生列表（支持keyword/status） |
| GET | /api/student/&lt;id&gt; | 学生详情 |
| POST | /api/student/add | 添加学生 |
| PUT | /api/student/update | 更新学生 |
| DELETE | /api/student/delete/&lt;id&gt; | 删除学生 |

### 入住管理
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/checkin/list | 入住记录列表 |
| POST | /api/checkin/check-in | 办理入住 |
| POST | /api/checkin/check-out/&lt;id&gt; | 办理退宿 |
| GET | /api/checkin/student/&lt;id&gt; | 学生入住记录 |

### 报修管理
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/repair/list | 报修列表（支持status筛选） |
| POST | /api/repair/submit | 提交报修 |
| POST | /api/repair/handle/&lt;id&gt; | 处理报修 |
| DELETE | /api/repair/delete/&lt;id&gt; | 删除报修 |
