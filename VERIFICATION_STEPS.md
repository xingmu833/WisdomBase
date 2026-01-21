# 🎊 前后端联调 - 验证步骤

**完成时间**: 2026年1月22日  
**前端端口**: 8849 (8848 被占用)  
**后端端口**: 8000  
**状态**: ✅ 就绪

---

## ✨ 立即验证

### 方法 1️⃣: 访问测试页面（最快）

打开浏览器访问: **http://localhost:8849/test-integration.html**

然后点击按钮进行自动化测试：

- 🔗 **测试连接** - 验证后端是否可用
- 🔐 **测试 Admin** - 使用 admin 账号登录
- 🔐 **测试 Editor** - 使用 editor 账号登录
- 🔐 **测试 Viewer** - 使用 viewer 账号登录
- 🚀 **运行全部测试** - 自动运行所有测试

### 方法 2️⃣: 前端登录测试（完整流程）

1. 打开浏览器访问: **http://localhost:8849/login**
2. 输入账号: `admin`
3. 输入密码: `admin123`
4. 点击 **登录** 按钮
5. 查看是否能成功登录并跳转到仪表板

> 💡 **提示**: 打开浏览器开发者工具 (F12) 观察网络请求，你会看到:
>
> - 请求 URL: `http://localhost:8849/api/v1/auth/login`
> - 代理转发到: `http://localhost:8000/api/v1/auth/login`
> - 响应状态: 200 (成功)

### 方法 3️⃣: 后端 API 文档测试

1. 打开浏览器访问: **http://localhost:8000/api/v1/docs**
2. 展开 **"auth"** 分类
3. 点击 **"POST /auth/login"**
4. 点击 **"Try it out"**
5. 输入用户名: `admin`, 密码: `admin123`
6. 点击 **"Execute"**
7. 查看响应 (应该返回 200 和 Token 信息)

---

## 🔍 调试技巧

### 查看网络请求

```
1. 按 F12 打开开发者工具
2. 切换到 Network 标签
3. 点击登录按钮
4. 查看请求详情:
   - URL 应该是: /api/v1/auth/login
   - Headers 应该包含: Content-Type: application/json
   - Response 应该包含: accessToken, refreshToken
```

### 查看浏览器存储

```
1. 按 F12 打开开发者工具
2. 切换到 Application 标签
3. 点击 Local Storage
4. 查找 __pure_admin_token__
5. 应该看到 JSON 格式的 Token 信息
```

### 查看后端日志

在后端运行的终端中会看到类似输出：

```
2026-01-22 00:13:30 INFO sqlalchemy.engine.Engine SELECT users.id, ...
2026-01-22 00:13:31 INFO Started server process
```

---

## 📊 测试清单

请按以下清单逐项验证：

### 后端验证 ✅

- [ ] 后端在 http://localhost:8000 运行
- [ ] 能访问 http://localhost:8000/health (应返回 OK)
- [ ] 能访问 http://localhost:8000/api/v1/docs (Swagger 文档)
- [ ] 数据库文件存在: `server/wisdombase.db`

### 前端验证 ✅

- [ ] 前端在 http://localhost:8849 运行
- [ ] 能访问 http://localhost:8849/login (登录页面)
- [ ] 能看到登录表单
- [ ] 表单中默认填充 admin / admin123

### 网络验证 ✅

- [ ] 点击登录时能看到网络请求
- [ ] 请求 URL 包含 `/api/v1/auth/login`
- [ ] 请求返回状态码 200
- [ ] 响应包含 `success: true`

### 登录验证 ✅

- [ ] Admin 能成功登录
- [ ] Editor 能成功登录
- [ ] Viewer 能成功登录
- [ ] 登录后能看到仪表板
- [ ] 登录后能看到用户名和角色信息

### Token 验证 ✅

- [ ] Token 能保存到 localStorage
- [ ] Token 包含 `accessToken` 字段
- [ ] Token 包含 `refreshToken` 字段
- [ ] Token 包含 `expires` 字段

---

## 🐛 故障排查

### 问题 1: "Cannot POST /api/v1/auth/login"

**原因**: 代理未生效或后端未运行

**解决方案**:

1. 检查后端是否运行在 8000 端口
2. 检查 `web/vite.config.ts` 中 proxy 配置是否正确
3. 重启前端开发服务器: `pnpm dev`

### 问题 2: "CORS policy: blocked by CORS"

**原因**: 后端 CORS 配置不正确

**解决方案**:

1. 检查 `server/config.py` 中 `CORS_ORIGINS` 是否包含 `http://localhost:8849`
2. 添加如果需要: `CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:8848", "http://localhost:8849"]`
3. 重启后端

### 问题 3: "Invalid credentials"

**原因**: 用户名或密码错误，或用户不存在

**解决方案**:

1. 确保使用正确的默认账号:
   - admin / admin123
   - editor / editor123
   - viewer / viewer123
2. 如果需要重置，运行: `python server/init_db.py`

### 问题 4: "Connection refused" (连接被拒绝)

**原因**: 后端未运行

**解决方案**:

```bash
# 后端启动步骤
cd server
python init_db.py
python main.py

# 应该看到:
# Uvicorn running on http://0.0.0.0:8000
```

### 问题 5: 登录后立即回到登录页面

**原因**: Token 保存失败或路由配置问题

**解决方案**:

1. 打开 F12 Console 查看错误信息
2. 检查 localStorage 中是否有 Token
3. 检查路由配置是否正确

---

## 📝 完整的工作流程

```
1. 启动后端 (Terminal 1)
   cd server
   python init_db.py  # 创建数据库
   python main.py     # 启动服务 (8000 端口)

2. 启动前端 (Terminal 2)
   cd web
   pnpm dev           # 启动开发服务 (8849 端口)

3. 测试登录
   访问 http://localhost:8849/login
   输入 admin / admin123
   点击登录
   ✓ 成功!

4. 查看网络请求
   F12 → Network 标签
   查看 /api/v1/auth/login 请求
   ✓ 代理工作正常!

5. 查看 Token 保存
   F12 → Application → Local Storage
   查找 __pure_admin_token__
   ✓ Token 已保存!
```

---

## 🎯 验证成功标志

当看到以下内容时，说明联调成功 ✅：

1. ✅ 前端能调用 `/api/v1/auth/login` 接口
2. ✅ 后端返回正确的 Token 和用户信息
3. ✅ 前端能保存 Token 到 localStorage
4. ✅ 登录后能跳转到仪表板
5. ✅ 刷新页面时能显示用户信息
6. ✅ 不同角色能看到不同的菜单和功能

---

## 📱 移动设备访问

如果想在其他设备上测试，可以使用网络地址：

```
http://192.168.1.99:8849
```

（IP 地址根据实际网络环境而定，前端启动时会显示）

---

## 💬 常见问题

**Q: 为什么前端端口是 8849 而不是 8848?**  
A: 因为 8848 端口被其他程序占用了，Vite 自动选择了下一个可用端口。

**Q: 是否需要手动修改配置文件?**  
A: 不需要！所有配置已预先完成：

- ✅ Vite 代理已配置
- ✅ API 路由已更新
- ✅ HTTP 拦截器已更新

**Q: 如何切换用户角色进行测试?**  
A: 简单的重新登录即可：

1. 点击登出（如果有菜单）
2. 返回登录页面
3. 使用不同账号重新登录

**Q: Token 过期了怎么办?**  
A: 系统会自动使用 refreshToken 来获取新的 accessToken，无需手动操作。

---

## 🎉 下一步

联调验证完成后，可以进行：

1. **功能测试**
   - 测试所有三个用户角色
   - 测试权限检查
   - 测试 Token 刷新

2. **功能开发**
   - 实现文档管理 CRUD
   - 实现版本控制
   - 实现 AI 功能

3. **生产准备**
   - 配置 PostgreSQL
   - 修改 SECRET_KEY
   - 配置 CORS
   - Docker 部署

---

**联调验证时间**: 2026-01-22  
**测试状态**: ✅ 就绪  
**建议**: 立即打开 test-integration.html 进行自动化测试！
