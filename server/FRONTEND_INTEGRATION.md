# WisdomBase 前端接口集成指南

## 修改前端的后端配置

### 1. 更新前端代理配置

修改 `web/vite.config.ts` 的proxy配置，连接到FastAPI后端：

```typescript
proxy: {
  "/api": {
    target: "http://localhost:8000",  // FastAPI后端地址
    changeOrigin: true,
    rewrite: (path) => path,
    // 如果需要移除/api前缀，可以使用：
    // rewrite: (path) => path.replace(/^\/api/, "")
  }
}
```

### 2. 更新HTTP请求工具

修改 `web/src/utils/http/index.ts` 中的token提取方式，使用Bearer token：

```typescript
// 在请求拦截器中
request.interceptors.request.use(
  (config) => {
    const token = getToken()?.accessToken;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error),
);
```

### 3. 更新登录接口

前端期望的登录响应格式与后端返回格式一致：

```typescript
// 前端 src/api/user.ts
export const getLogin = (data?: object) => {
  return http.request<UserResult>("post", "/api/v1/auth/login", { data });
};
```

### 4. 刷新Token逻辑

后端的token刷新接口返回新的access_token，前端需要更新。在HTTP拦截器中处理401响应：

```typescript
// 在响应拦截器中处理401错误
response.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // 调用刷新token接口
      const refreshToken = getToken()?.refreshToken;
      if (refreshToken) {
        try {
          const result = await http.request(
            "post",
            "/api/v1/auth/refresh-token",
            {
              data: { refreshToken },
            },
          );
          // 更新token
          setToken(result.data);
          // 重试原请求
          return http.request(/* ... */);
        } catch (e) {
          // 刷新失败，重定向到登录
          router.push("/login");
        }
      }
    }
    return Promise.reject(error);
  },
);
```

## 修改前端mock数据

### 移除Mock数据

在开发时连接到真实后端，可以注释或删除 `web/mock` 目录下的文件。

或者在 `web/vite.config.ts` 中禁用mock插件：

```typescript
import { viteMockServe } from "vite-plugin-fake-server";

plugins: [
  viteMockServe({
    // 条件：false表示在此模式下禁用mock
    mockPath: process.env.NODE_ENV === "production" ? "" : "mock",
  }),
];
```

## 角色权限对应关系

### Admin (管理员)

```json
{
  "roles": ["admin"],
  "permissions": [
    "*:*:*", // 全部权限
    "document:create",
    "document:read",
    "document:update",
    "document:delete",
    "user:manage",
    "user:read",
    "log:view",
    "version:rollback",
    "ai:call",
    "qa:use"
  ]
}
```

### Editor (编辑者)

```json
{
  "roles": ["editor"],
  "permissions": [
    "document:create",
    "document:read",
    "document:update",
    "version:rollback",
    "ai:call"
  ]
}
```

### Viewer (访客)

```json
{
  "roles": ["viewer"],
  "permissions": ["document:read", "qa:use"]
}
```

## 前端权限检查示例

### 使用v-auth指令

```vue
<!-- 仅Admin可见 -->
<button v-auth="['user:manage']">用户管理</button>

<!-- 仅Editor和Admin可见 -->
<button v-auth="['document:update']">编辑文档</button>

<!-- 仅Viewer及以上可见 -->
<button v-auth="['document:read']">查看文档</button>
```

### 使用权限检查函数

```typescript
import { hasAuth } from "@/router/utils";

if (hasAuth("user:manage")) {
  // 显示用户管理界面
}
```

## 环境配置

### 开发环境 (.env.development)

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_PUBLIC_PATH=/
```

### 生产环境 (.env.production)

```env
VITE_API_BASE_URL=https://api.wisdombase.com
VITE_PUBLIC_PATH=/
```

## 测试流程

1. **启动后端**

   ```bash
   cd server
   python init_db.py
   python main.py
   ```

2. **启动前端**

   ```bash
   cd web
   pnpm install
   pnpm dev
   ```

3. **测试登录**
   - 访问 http://localhost:5173/login
   - 使用以下凭证登录：
     - 管理员: admin / admin123
     - 编辑者: editor / editor123
     - 访客: viewer / viewer123

4. **测试权限**
   - 以不同身份登录，验证功能菜单和按钮的显示

## 常见问题

### 1. CORS错误

如果遇到CORS错误，检查后端的CORS配置 (`config.py`)：

```python
CORS_ORIGINS: list = [
    "http://localhost:5173",  # 前端地址
    "http://localhost:3000"
]
```

### 2. Token过期处理

后端的access_token过期时间默认为120分钟。前端应该：

- 监听401响应
- 调用refresh-token接口
- 使用新token重试请求

### 3. 密钥安全

生产环境必须修改 `SECRET_KEY` 值，并将其存储在安全的地方（如环境变量）。

## 相关文件更新清单

- [ ] `web/vite.config.ts` - 更新proxy配置
- [ ] `web/src/utils/http/index.ts` - 更新Authorization header
- [ ] `web/src/api/user.ts` - 确认API端点
- [ ] `web/.env` - 配置API地址
- [ ] 移除或禁用 `web/mock/` 文件

## 下一步

1. 完成文档管理API
2. 实现版本控制
3. 集成AI功能
4. 添加问答功能
5. 编写完整的单元测试和集成测试
