# WisdomBase API - FastAPI 后端

这是一个基于FastAPI的知识库系统后端API。

## 功能特性

### 1. 用户认证与授权

- **JWT Token认证** - 使用access_token和refresh_token机制
- **三种用户角色**:
  - **Admin (管理员)** - 完全权限，可以CRUD所有文档、用户管理、查看操作日志
  - **Editor (编辑者)** - 可以CRUD自身创建的文档、读取所有文档、版本回滚、调用AI功能
  - **Viewer (访客)** - 只读已发布文档、使用问答功能
- **密码加密** - 使用bcrypt进行密码哈希

### 2. 用户管理

- 创建、读取、更新、删除用户（仅管理员）
- 用户激活/禁用
- 角色分配
- 权限自动生成

### 3. 操作日志

- 记录所有关键操作（登录、登出、CRUD操作）
- 支持按用户、操作类型、资源类型过滤
- 仅管理员可查看

### 4. 文档管理（预留接口）

- 文档创建、读取、更新、删除
- 文档发布/草稿管理
- 版本控制和回滚

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 初始化数据库

```bash
python init_db.py
```

这将创建SQLite数据库和三个默认用户：

- **admin** / admin123
- **editor** / editor123
- **viewer** / viewer123

### 启动服务器

#### 开发环境

```bash
python main.py
```

或使用uvicorn：

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 生产环境

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

访问API文档：http://localhost:8000/api/v1/docs

## API 端点

### 认证 (`/api/v1/auth`)

- `POST /login` - 用户登录
- `POST /refresh-token` - 刷新access token
- `POST /logout` - 用户登出
- `GET /me` - 获取当前用户信息

### 用户管理 (`/api/v1/users`)

- `GET /` - 获取用户列表（管理员）
- `GET /{user_id}` - 获取用户详情（管理员）
- `POST /` - 创建新用户（管理员）
- `PUT /{user_id}` - 更新用户信息（管理员）
- `DELETE /{user_id}` - 删除用户（管理员）
- `PUT /{user_id}/status` - 切换用户状态（管理员）

### 操作日志 (`/api/v1/logs`)

- `GET /` - 获取操作日志列表（管理员）
- `GET /{log_id}` - 获取日志详情（管理员）
- `GET /user/{user_id}` - 获取用户的操作日志（管理员）
- `DELETE /{log_id}` - 删除日志（管理员）
- `DELETE /` - 批量删除日志（管理员）

## 环境配置

创建 `.env` 文件配置以下变量：

```env
# FastAPI配置
APP_NAME=WisdomBase API
APP_VERSION=1.0.0
DEBUG=True
API_PREFIX=/api/v1

# 数据库配置
DATABASE_URL=sqlite:///./wisdombase.db

# JWT配置
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120
REFRESH_TOKEN_EXPIRE_DAYS=30

# CORS配置
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
CORS_CREDENTIALS=True
```

## 数据库迁移

### 使用Alembic进行迁移（可选）

```bash
# 初始化Alembic
alembic init alembic

# 生成迁移脚本
alembic revision --autogenerate -m "Initial migration"

# 应用迁移
alembic upgrade head
```

## 部署到生产环境

### 切换到PostgreSQL

1. 更新 `.env` 文件：

```env
DATABASE_URL=postgresql://user:password@localhost/wisdombase
```

2. 安装PostgreSQL驱动：

```bash
pip install psycopg2-binary
```

3. 运行数据库迁移

### 使用Docker

```bash
# 构建镜像
docker build -t wisdombase-api .

# 运行容器
docker run -p 8000:8000 wisdombase-api
```

### 使用Gunicorn + Nginx

```bash
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

## 项目结构

```
server/
├── config.py              # 配置文件
├── database.py            # 数据库配置
├── models.py              # SQLAlchemy模型
├── schemas.py             # Pydantic模式
├── security.py            # 安全认证相关
├── enums.py              # 枚举定义
├── dependencies.py        # 依赖注入
├── main.py               # FastAPI应用入口
├── init_db.py            # 数据库初始化脚本
├── requirements.txt      # Python依赖
└── routes/               # 路由模块
    ├── auth.py          # 认证路由
    ├── users.py         # 用户管理路由
    └── logs.py          # 操作日志路由
```

## 开发计划

- [ ] 文档管理API
- [ ] 文档版本控制
- [ ] 问答功能
- [ ] AI功能集成
- [ ] 权限细粒度控制
- [ ] 审计日志
- [ ] API限流
- [ ] 缓存机制
- [ ] 完整的单元测试和集成测试

## 测试

### 登录示例

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### 使用Token访问受保护的端点

```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer <access_token>"
```

## 许可证

MIT

## 支持

如有问题，请提交Issue或联系维护者。
