# 🚀 WisdomBase 快速启动指南

## 项目概述

WisdomBase是一个基于**Vue 3 + Pure Admin Thin**前端框架和**FastAPI**后端的企业级知识管理系统。支持三种用户角色（Admin、Editor、Viewer），具有完整的权限控制和操作审计功能。

---

## 📋 系统要求

- **Node.js** >= 16.x
- **Python** >= 3.9
- **npm/pnpm** 或 **pip**
- **PostgreSQL** 或 **SQLite**

---

## 🏗️ 后端快速启动（FastAPI）

### 1️⃣ 安装依赖

```bash
cd server
pip install -r requirements.txt
```

### 2️⃣ 初始化数据库

```bash
python init_db.py
```

✅ 创建SQLite数据库和3个测试用户

### 3️⃣ 启动后端服务

```bash
python main.py
```

- 服务运行在：**http://localhost:8000**
- API文档：**http://localhost:8000/api/v1/docs** (Swagger UI)
- 健康检查：**http://localhost:8000/health**

### 默认测试账号

| 角色   | 用户名 | 密码      | 权限             |
| ------ | ------ | --------- | ---------------- |
| 管理员 | admin  | admin123  | 全部             |
| 编辑者 | editor | editor123 | 文档CRUD、AI调用 |
| 访客   | viewer | viewer123 | 只读、问答       |

---

## 🎨 前端快速启动（Vue 3）

### 1️⃣ 安装依赖

```bash
cd web
pnpm install
# 或 npm install
```

### 2️⃣ 配置后端代理

✅ **已预先配置** - 无需手动修改！

Vite 已配置代理，所有 `/api/*` 请求会自动转向后端 `http://localhost:8000`

配置位置：`web/vite.config.ts`

### 3️⃣ 启动开发服务器

```bash
pnpm dev
```

- 前端运行在：**http://localhost:8848** (若 8848 被占用，则使用 8849)
- 自动打开浏览器

### 4️⃣ 登录测试

访问 http://localhost:8848/login，使用上述默认账号登录

---

## 🔗 前后端联调验证

### ✅ 已完成的联调配置

| 项目        | 配置                         | 状态 |
| ----------- | ---------------------------- | ---- |
| Vite 代理   | `/api/*` 转向后端            | ✅   |
| 登录接口    | `/api/v1/auth/login`         | ✅   |
| Token 刷新  | `/api/v1/auth/refresh-token` | ✅   |
| HTTP 白名单 | 已更新                       | ✅   |

### 📊 联调架构

```
前端 (8848/8849)
    ↓
Vite 代理
    ↓
后端 (8000)
    ↓
SQLite 数据库
```

详见：[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)

## 🔐 三种用户角色详解

### 👑 Admin（管理员）

**权限**：`*:*:*`（全部权限）

**功能**：

- ✅ CRUD所有文档
- ✅ 用户管理（创建、删除、禁用）
- ✅ 查看所有操作日志
- ✅ 文档版本回滚
- ✅ AI功能调用

**访问**: 所有菜单和功能

---

### ✏️ Editor（编辑者）

**权限**：`["document:create", "document:read", "document:update", "version:rollback", "ai:call"]`

**功能**：

- ✅ 创建并编辑自己的文档
- ✅ 读取所有已发布文档
- ✅ 文档版本回滚
- ✅ 调用AI功能

**限制**：

- ❌ 无法管理其他用户
- ❌ 无法查看操作日志
- ❌ 无法删除他人文档

---

### 👁️ Viewer（访客）

**权限**：`["document:read", "qa:use"]`

**功能**：

- ✅ 查看所有已发布文档
- ✅ 使用问答（Q&A）功能

**限制**：

- ❌ 无法编辑文档
- ❌ 无法创建文档
- ❌ 无法访问AI功能

---

## 🔌 API 端点速查

### 认证 (Authentication)

```bash
# 登录
POST /api/v1/auth/login
{
  "username": "admin",
  "password": "admin123"
}

# 刷新Token
POST /api/v1/auth/refresh-token
{
  "refreshToken": "eyJ..."
}

# 获取当前用户信息
GET /api/v1/auth/me
Header: Authorization: Bearer <access_token>

# 登出
POST /api/v1/auth/logout
```

### 用户管理 (Users - Admin Only)

```bash
# 获取用户列表
GET /api/v1/users?skip=0&limit=10

# 创建用户
POST /api/v1/users
{
  "username": "newuser",
  "password": "pass123",
  "email": "user@example.com",
  "nickname": "用户名",
  "roles": ["editor"]
}

# 更新用户
PUT /api/v1/users/{user_id}

# 删除用户
DELETE /api/v1/users/{user_id}

# 切换用户状态
PUT /api/v1/users/{user_id}/status
```

### 操作日志 (Logs - Admin Only)

```bash
# 获取日志列表
GET /api/v1/logs?skip=0&limit=20

# 按用户获取日志
GET /api/v1/logs/user/{user_id}

# 获取特定日志
GET /api/v1/logs/{log_id}

# 删除日志
DELETE /api/v1/logs/{log_id}
```

---

## 🗂️ 项目结构

```
WisdomBase/
├── server/              # FastAPI后端
│   ├── main.py         # 应用入口
│   ├── config.py       # 配置文件
│   ├── models.py       # 数据库模型
│   ├── schemas.py      # 请求/响应模式
│   ├── security.py     # JWT、密码处理
│   ├── enums.py        # 角色权限定义
│   ├── init_db.py      # 数据库初始化
│   ├── routes/
│   │   ├── auth.py     # 认证路由
│   │   ├── users.py    # 用户管理路由
│   │   └── logs.py     # 日志路由
│   ├── requirements.txt # Python依赖
│   ├── Dockerfile      # Docker配置
│   └── docker-compose.yml # Docker Compose配置
│
└── web/                 # Vue 3前端
    ├── src/
    │   ├── main.ts     # 应用入口
    │   ├── router/     # 路由配置
    │   ├── store/      # Pinia状态管理
    │   ├── components/ # 组件库
    │   ├── directives/ # 自定义指令
    │   ├── api/        # API调用
    │   └── utils/      # 工具函数
    ├── vite.config.ts  # Vite配置
    ├── package.json    # 依赖配置
    └── pnpm-lock.yaml  # 依赖锁定
```

---

## 🔄 完整开发流程

### 同时启动前后端

```bash
# 终端1 - 启动后端
cd server
python init_db.py
python main.py

# 终端2 - 启动前端
cd web
pnpm dev
```

### 测试登录流程

1. 访问 http://localhost:5173/login
2. 使用账号 `admin` / `admin123` 登录
3. 查看菜单和功能是否正常加载
4. 切换用户角色测试权限

### 切换到不同用户角色

```bash
# 重新初始化数据库（可选）
cd server
python init_db.py

# 然后用不同账号登录测试
```

---

## 🔧 环境配置

### 后端配置 (`server/.env`)

```env
# 应用配置
APP_NAME=WisdomBase API
DEBUG=True

# 数据库配置（开发环境）
DATABASE_URL=sqlite:///./wisdombase.db

# JWT配置
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120

# CORS配置
CORS_ORIGINS=["http://localhost:5173"]
```

### 前端配置 (`web/.env.development`)

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_PUBLIC_PATH=/
```

---

## 📦 部署到生产环境

### 后端部署 (使用Docker)

```bash
cd server
docker-compose up -d
```

配置PostgreSQL数据库：

```env
DATABASE_URL=postgresql://user:password@localhost:5432/wisdombase
```

### 前端构建

```bash
cd web
pnpm build  # 生成dist/文件夹
```

### Nginx配置示例

```nginx
server {
    listen 80;
    server_name wisdombase.com;

    location / {
        root /var/www/wisdombase/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
    }
}
```

---

## 🐛 常见问题

### Q: CORS错误怎么办？

**A:** 检查 `server/config.py` 的 `CORS_ORIGINS` 配置，确保包含前端地址：

```python
CORS_ORIGINS: list = ["http://localhost:5173"]
```

### Q: Token过期无法自动刷新？

**A:** 确保前端HTTP拦截器实现了token刷新逻辑（见 `server/FRONTEND_INTEGRATION.md`）

### Q: 数据库连接错误？

**A:**

- 确保SQLite文件有写入权限
- 或切换到PostgreSQL：`DATABASE_URL=postgresql://...`

### Q: 如何测试不同权限？

**A:** 使用不同的用户账号登录：

- `admin` - 查看完整功能
- `editor` - 查看编辑功能
- `viewer` - 查看只读功能

---

## 📚 相关文档

- [后端集成指南](server/README.md) - 详细API文档
- [前端集成指南](server/FRONTEND_INTEGRATION.md) - 前端配置说明
- [Copilot指南](.github/copilot-instructions.md) - AI开发辅助

---

## ✨ 功能清单

- [x] 用户认证 (JWT Token)
- [x] 三种用户角色 (Admin, Editor, Viewer)
- [x] 基于角色的权限控制 (RBAC)
- [x] 用户管理 (CRUD)
- [x] 操作日志审计
- [x] Token自动刷新
- [ ] 文档CRUD (计划中)
- [ ] 文档版本控制 (计划中)
- [ ] AI功能集成 (计划中)
- [ ] Q&A功能 (计划中)

---

## 📞 支持与反馈

如有任何问题，请：

1. 查看相关文档
2. 检查错误日志
3. 提交Issue

祝你开发愉快！🎉
