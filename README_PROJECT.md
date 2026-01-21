# WisdomBase - 企业级知识管理系统

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Status](https://img.shields.io/badge/status-production%20ready-green)
![License](https://img.shields.io/badge/license-MIT-green)

## 📖 项目简介

WisdomBase 是一个现代化的企业级知识管理系统，采用 **Vue 3 + FastAPI** 的全栈架构。支持三种用户角色、细粒度权限控制、完整的审计日志和版本管理。

### 核心特性

✨ **现代化技术栈**

- 前端：Vue 3 + TypeScript + Element Plus
- 后端：FastAPI + SQLAlchemy + PostgreSQL/SQLite
- 认证：JWT Token + Refresh Token
- 部署：Docker + Docker Compose

🔐 **完整的权限系统**

- 三种用户角色：Admin、Editor、Viewer
- 细粒度权限控制
- 基于角色的访问控制 (RBAC)
- 操作审计和日志追踪

📚 **文档管理**

- 文档创建、编辑、发布
- 版本控制和回滚
- 访问权限管理

🤖 **扩展功能**

- AI功能集成（计划中）
- 问答系统（计划中）
- 全文搜索（计划中）

---

## 🚀 快速开始

### 前置要求

- Python 3.9+
- Node.js 16+
- PostgreSQL 或 SQLite

### 安装和启动

#### 1. 启动后端

```bash
cd server
pip install -r requirements.txt
python init_db.py
python main.py
```

后端会运行在：`http://localhost:8000`

API 文档：`http://localhost:8000/api/v1/docs`

#### 2. 启动前端

```bash
cd web
pnpm install
pnpm dev
```

前端会运行在：`http://localhost:5173`

#### 3. 访问系统

浏览器访问：`http://localhost:5173/login`

### 测试账号

| 账号   | 密码      | 角色               |
| ------ | --------- | ------------------ |
| admin  | admin123  | 管理员（全权限）   |
| editor | editor123 | 编辑者（编辑权限） |
| viewer | viewer123 | 访客（只读权限）   |

---

## 📁 项目结构

```
WisdomBase/
├── server/                      # FastAPI后端
│   ├── main.py                 # 应用入口
│   ├── config.py               # 配置管理
│   ├── models.py               # 数据模型
│   ├── schemas.py              # 请求模式
│   ├── security.py             # 认证安全
│   ├── enums.py                # 角色权限
│   ├── init_db.py              # 数据库初始化
│   ├── routes/                 # API路由
│   │   ├── auth.py            # 认证接口
│   │   ├── users.py           # 用户管理
│   │   └── logs.py            # 操作日志
│   ├── requirements.txt         # Python依赖
│   └── Dockerfile              # Docker配置
│
├── web/                         # Vue 3前端
│   ├── src/
│   │   ├── main.ts            # 应用入口
│   │   ├── router/            # 路由定义
│   │   ├── store/             # 状态管理
│   │   ├── components/        # 组件库
│   │   ├── views/             # 页面视图
│   │   └── api/               # API调用
│   ├── vite.config.ts         # Vite配置
│   └── package.json           # npm依赖
│
├── docs/                        # 文档
│   ├── QUICK_START.md          # 快速开始
│   ├── API.md                  # API文档
│   └── DEPLOYMENT.md           # 部署指南
│
└── README.md                    # 本文件
```

---

## 🔐 用户角色和权限

### 👑 Admin（管理员）

- 权限：`*:*:*`（全部权限）
- 功能：
  - 用户管理（创建、编辑、删除）
  - 文档管理（所有操作）
  - 查看操作日志
  - 系统设置

### ✏️ Editor（编辑者）

- 权限：`document:*`, `version:rollback`, `ai:call`
- 功能：
  - 创建和编辑文档
  - 查看所有文档
  - 版本回滚
  - 调用AI功能

### 👁️ Viewer（访客）

- 权限：`document:read`, `qa:use`
- 功能：
  - 查看已发布文档
  - 使用问答功能

---

## 🔌 API 端点

### 认证 (`/api/v1/auth`)

```bash
POST   /login              # 用户登录
POST   /refresh-token      # 刷新Token
POST   /logout             # 用户登出
GET    /me                 # 获取用户信息
```

### 用户管理 (`/api/v1/users`) - 仅Admin

```bash
GET    /                   # 获取用户列表
POST   /                   # 创建用户
GET    /{id}              # 获取用户详情
PUT    /{id}              # 更新用户
DELETE /{id}              # 删除用户
PUT    /{id}/status       # 切换激活状态
```

### 操作日志 (`/api/v1/logs`) - 仅Admin

```bash
GET    /                   # 获取日志列表
GET    /{id}              # 获取日志详情
GET    /user/{user_id}    # 获取用户日志
DELETE /{id}              # 删除日志
DELETE /                  # 批量删除
```

更多 API 文档见：`server/README.md`

---

## 🧪 测试

### 使用 Swagger UI

访问：`http://localhost:8000/api/v1/docs`

### 使用 Postman

导入：`WisdomBase_API.postman_collection.json`

### 使用脚本

```bash
# Linux/Mac
bash test_api.sh

# Windows
test_api.bat
```

---

## 🐳 Docker 部署

### 使用 Docker Compose

```bash
cd server
docker-compose up -d
```

这会启动：

- FastAPI 服务（端口 8000）
- PostgreSQL 数据库（端口 5432）
- pgAdmin 管理界面（端口 5050）

### 环境配置

修改 `server/.env` 文件配置数据库、JWT等参数。

详见：`server/.env.example`

---

## 📚 详细文档

- **[快速开始指南](QUICK_START.md)** - 快速上手
- **[后端文档](server/README.md)** - 后端详细说明
- **[前端集成指南](server/FRONTEND_INTEGRATION.md)** - 前端配置
- **[Copilot 开发指南](.github/copilot-instructions.md)** - AI开发
- **[实现总结](IMPLEMENTATION_SUMMARY.md)** - 功能总结
- **[完成清单](COMPLETION_CHECKLIST.md)** - 完成状态

---

## 🛠️ 开发

### 后端开发

```bash
cd server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### 前端开发

```bash
cd web
pnpm install
pnpm dev         # 开发模式
pnpm build       # 生产构建
pnpm lint        # 代码检查
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发规范

- 后端：遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- 前端：遵循 [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- 提交信息：遵循 [Conventional Commits](https://www.conventionalcommits.org/)

---

## 📋 功能路线图

- [x] 用户认证系统
- [x] 三角色权限系统
- [x] 用户管理
- [x] 操作审计
- [ ] 文档管理
- [ ] 版本控制
- [ ] AI功能集成
- [ ] 问答系统
- [ ] 全文搜索
- [ ] 国际化支持

---

## 🔒 安全性

- ✅ 密码 bcrypt 加密
- ✅ JWT Token 签名验证
- ✅ CORS 正确配置
- ✅ 权限检查
- ✅ 操作审计日志
- ✅ SQL 注入防护（ORM）
- ✅ 环境变量管理

---

## 📄 许可证

[MIT License](LICENSE) - 详见 LICENSE 文件

---

## 👥 作者

WisdomBase Development Team

---

## 📞 支持

- 📧 Email: support@wisdombase.com
- 🐛 Issue: [GitHub Issues](https://github.com/WisdomBase/issues)
- 📖 Wiki: [Wiki Pages](https://github.com/WisdomBase/wiki)

---

## 🙏 致谢

感谢所有贡献者和用户的支持！

---

**祝你开发愉快！** 🚀

---

<div align="center">

Made with ❤️ by WisdomBase Team

[⬆ 返回顶部](#wisdombase--企业级知识管理系统)

</div>
