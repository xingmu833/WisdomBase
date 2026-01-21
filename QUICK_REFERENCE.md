# ⚡ 联调快速参考卡

## 🚀 启动命令

### 后端启动（Terminal 1）

```bash
cd server
python init_db.py
python main.py
```

### 前端启动（Terminal 2）

```bash
cd web
pnpm dev
```

---

## 🌐 访问地址

| 服务     | 地址                                        | 用途       |
| -------- | ------------------------------------------- | ---------- |
| 前端     | http://localhost:8849                       | 主应用     |
| 后端     | http://localhost:8000                       | API 服务   |
| API 文档 | http://localhost:8000/api/v1/docs           | Swagger    |
| 测试工具 | http://localhost:8849/test-integration.html | 自动化测试 |

---

## 👤 默认账号

```
Account    Password    Role
admin      admin123    Admin      (All permissions)
editor     editor123   Editor     (Edit only)
viewer     viewer123   Viewer     (Read only)
```

---

## 📝 修改概览

### 后端 (2 files)

```
✅ server/main.py
   - Import routes module
   - Register routes

✅ server/routes/routes.py (NEW)
   - GET /api/v1/routes/async
```

### 前端 (4 files)

```
✅ web/vite.config.ts
   - Add /api proxy

✅ web/src/api/user.ts
   - /login → /api/v1/auth/login
   - /refresh-token → /api/v1/auth/refresh-token

✅ web/src/api/routes.ts
   - /get-async-routes → /api/v1/routes/async

✅ web/src/utils/http/index.ts
   - Update whitelist URLs
```

---

## 🔗 API 端点

### Auth (认证)

```
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh-token
GET    /api/v1/auth/me
POST   /api/v1/auth/logout
```

### Users (用户管理 - Admin only)

```
GET    /api/v1/users
POST   /api/v1/users
PUT    /api/v1/users/{id}
DELETE /api/v1/users/{id}
PUT    /api/v1/users/{id}/status
```

### Logs (日志管理 - Admin only)

```
GET    /api/v1/logs
GET    /api/v1/logs/{id}
GET    /api/v1/logs/user/{user_id}
DELETE /api/v1/logs/{id}
DELETE /api/v1/logs
```

### Routes (路由)

```
GET    /api/v1/routes/async
```

---

## 🧪 快速测试

### Swagger UI 测试

1. 访问 http://localhost:8000/api/v1/docs
2. 展开 auth → POST /auth/login
3. 点击 Try it out
4. 输入 admin / admin123
5. 点击 Execute

### 前端登录测试

1. 访问 http://localhost:8849/login
2. 输入 admin / admin123
3. 点击登录

### 自动化测试

1. 访问 http://localhost:8849/test-integration.html
2. 点击运行全部测试

---

## 🔍 调试

### 查看网络请求

```
F12 → Network → 查看 /api/v1/auth/login
```

### 查看存储

```
F12 → Application → Local Storage → 查找 __pure_admin_token__
```

### 查看日志

```
后端 Terminal → 查看 SQL 操作和 HTTP 请求日志
```

---

## ⚙️ 代理原理

```
浏览器: http://localhost:8849/api/v1/auth/login
    ↓
Vite 代理检查
    ↓
/api → http://localhost:8000
    ↓
后端: http://localhost:8000/api/v1/auth/login
```

---

## 📊 系统状态

- 后端: ✅ 运行中 (8000)
- 前端: ✅ 运行中 (8849)
- 数据库: ✅ 初始化完成
- 代理: ✅ 配置完成
- CORS: ✅ 配置完成

---

## 🐛 常见问题

| 问题       | 解决方案                     |
| ---------- | ---------------------------- |
| CORS 错误  | 检查 CORS_ORIGINS 配置       |
| 404 错误   | 检查后端是否运行             |
| 登录失败   | 检查用户名/密码是否正确      |
| Token 问题 | 检查 localStorage 中的 Token |
| 代理不工作 | 重启前端: pnpm dev           |

---

## 📚 相关文档

- [QUICK_START.md](./QUICK_START.md)
- [INTEGRATION_GUIDE.md](./INTEGRATION_GUIDE.md)
- [VERIFICATION_STEPS.md](./VERIFICATION_STEPS.md)
- [server/README.md](./server/README.md)

---

**备注**: 所有配置已预设完成，可直接启动使用！
