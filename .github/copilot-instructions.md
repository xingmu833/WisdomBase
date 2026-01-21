# Copilot Instructions for WisdomBase

**Project:** Vue 3 + Pure Admin Thin - Enterprise Admin Dashboard Framework  
**Type:** Full-Stack SPA with FastAPI backend, Pinia state management, dynamic routing

## Frontend Architecture Overview

### Core Stack (Web)

- **Framework**: Vue 3 + TypeScript + Vite
- **State**: Pinia (see `web/src/store/modules/`) with store hooks pattern (e.g., `useAppStoreHook()`)
- **Routing**: Vue Router 4 with auto-imported modules from `web/src/router/modules/*.ts`
- **UI**: Element Plus + @pureadmin/table + Tailwind CSS
- **HTTP**: Axios wrapper at `web/src/utils/http/index.ts` with JWT token refresh
- **Icons**: Iconify + offline icons

### Key Data Flows

1. **Auth**: Login → `POST /api/v1/auth/login` → Store access/refresh tokens → Route to dashboard
2. **Permissions**: User roles loaded → Check against `v-auth` directives → Menu rendered
3. **Token Refresh**: Interceptor detects 401 → `POST /api/v1/auth/refresh-token` → Retry request

### Frontend Directory Structure

- `web/src/store/modules/` - Pinia stores (app, permission, user, multiTags, settings, epTheme)
- `web/src/router/modules/` - Auto-imported route definitions (flatten to 2-level)
- `web/src/layout/components/` - Layout sub-components (navbar, sidebar, content, tag, setting)
- `web/src/components/Re*` - Reusable components with `index.ts` exports
- `web/src/directives/` - Custom directives (auth, copy, longpress, perms, ripple)
- `web/mock/` - Development mock data (replace with real endpoints)

## Frontend Key Patterns

### Store Usage

```typescript
import { useAppStoreHook } from "@/store/modules/app";
const appStore = useAppStoreHook();
appStore.getSidebarStatus; // getter
appStore.TOGGLE_SIDEBAR(); // action
```

### Permission Control

```vue
<!-- v-auth removes element if user lacks permission -->
<button v-auth="['user:manage']">User Admin</button>

<!-- Perms component wrapper -->
<Perms :auth="['document:update']">
  <button>Edit Document</button>
</Perms>
```

### Adding Routes

1. Create `web/src/router/modules/[feature].ts` with `RouteRecordRaw` default export
2. Auto-imported; add `meta.icon`, `meta.title` for menu generation
3. Routes flatten to 2-level max automatically

---

# FastAPI Backend Architecture

**Backend Stack**: FastAPI + SQLAlchemy + JWT + SQLite/PostgreSQL

## Backend Project Structure

- `server/config.py` - Configuration (database, JWT, CORS)
- `server/models.py` - SQLAlchemy ORM models (User, Document, OperationLog, DocumentVersion)
- `server/schemas.py` - Pydantic request/response schemas
- `server/security.py` - JWT creation/verification, password hashing with bcrypt
- `server/database.py` - Database session management
- `server/enums.py` - Role and permission definitions with mappings
- `server/main.py` - FastAPI app entry, CORS middleware, route registration
- `server/routes/` - API routes (auth.py, users.py, logs.py)
- `server/init_db.py` - Create database + 3 test users

## Database Models

### User

- `username`, `email` (unique), `roles` (JSON), `permissions` (JSON)
- `is_active`, `last_login` tracking
- Relations: documents, operation_logs

### OperationLog

- Tracks CREATE/READ/UPDATE/DELETE/LOGIN/LOGOUT actions
- Records user_id, resource_type, resource_id, description, IP address
- Indexed by created_at for efficient filtering

### Document (structure defined, endpoints not yet implemented)

- `title`, `content`, `author_id` (FK), `is_published` flag
- Relations: author (User), versions (DocumentVersion)

### DocumentVersion (structure defined)

- Version control with version_number
- Composite index: (document_id, version_number)

## Authentication & Authorization

### JWT Token Flow

1. **Login** `POST /api/v1/auth/login` → returns `accessToken` (2hr) + `refreshToken` (30d)
2. **Refresh** `POST /api/v1/auth/refresh-token` with refreshToken → new accessToken
3. **Protected** Require header: `Authorization: Bearer <accessToken>`

### Role-Based Permissions

```python
Admin    ["*:*:*", "document:*", "user:manage", "log:view", ...]
Editor   ["document:create", "document:read", "document:update", "version:rollback", "ai:call"]
Viewer   ["document:read", "qa:use"]
```

### Default Test Credentials

- `admin` / `admin123` (all permissions)
- `editor` / `editor123` (document editing + AI)
- `viewer` / `viewer123` (read-only + QA)

## API Endpoints

### Auth (`/api/v1/auth`)

- `POST /login` - Returns tokens + user info
- `POST /refresh-token` - Exchange refreshToken → new accessToken
- `POST /logout` - Record logout event
- `GET /me` - Current user profile

### Users (`/api/v1/users`, admin-only)

- `GET /` - List all users (paginated, skip/limit)
- `POST /` - Create user (auto-assign permissions by role)
- `PUT /{user_id}` - Update email/nickname/avatar/roles
- `DELETE /{user_id}` - Delete user
- `PUT /{user_id}/status` - Toggle is_active flag

### Logs (`/api/v1/logs`, admin-only)

- `GET /` - List with filters: user_id, action, resource_type
- `GET /{log_id}` - Single log detail
- `GET /user/{user_id}` - All logs for user
- `DELETE /{log_id}` - Delete log
- `DELETE /` - Batch delete logs

## Development Workflow

### Backend Setup

```bash
cd server
pip install -r requirements.txt
python init_db.py              # Creates wisdombase.db + 3 test users
python main.py                 # Runs on http://localhost:8000
# Swagger docs: http://localhost:8000/api/v1/docs
```

### Environment Config (`.env`)

```env
DATABASE_URL=sqlite:///./wisdombase.db
SECRET_KEY=your-secret-key-change-this
ACCESS_TOKEN_EXPIRE_MINUTES=120
CORS_ORIGINS=["http://localhost:5173"]
```

### Production Database Switch (PostgreSQL)

```env
DATABASE_URL=postgresql://user:password@localhost/wisdombase
```

### Docker Deployment

```bash
docker-compose up -d
# FastAPI: http://localhost:8000
# PostgreSQL: localhost:5432
# pgAdmin: http://localhost:5050
```

## Frontend Integration

### Modify Proxy (web/vite.config.ts)

```typescript
proxy: {
  "/api": {
    target: "http://localhost:8000",
    changeOrigin: true
  }
}
```

### Update HTTP Client (web/src/utils/http/index.ts)

```typescript
// In request interceptor:
if (token?.accessToken) {
  config.headers.Authorization = `Bearer ${token.accessToken}`;
}

// In response interceptor (handle 401):
if (error.response?.status === 401) {
  const result = await refreshToken();
  setToken(result.data);
  return retryRequest();
}
```

### Switch Off Mock Data

- Remove mock files or comment out `viteMockServe` plugin in vite.config.ts
- API endpoints auto-connect to `/api/v1/*` backend

## Common Backend Patterns

### Adding Endpoints

1. Create route file `server/routes/feature.py`
2. Define Pydantic schemas in `server/schemas.py`
3. Add dependency: `async def require_admin(current_user: User = Depends(get_current_user))`
4. Include in main.py: `app.include_router(router, prefix=settings.API_PREFIX)`

### Permission Checks

```python
# Admin-only
async def admin_only(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    return {"user_id": current_user.id}

# Check specific permission
@app.get("/protected")
async def protected(
    _: bool = Depends(check_permission("user:manage"))
):
    pass
```

### Log Operations

```python
log = OperationLog(
    user_id=current_user.id,
    action="CREATE",
    resource_type="document",
    resource_id=doc_id,
    description="Document created",
    ip_address=get_client_ip(request)
)
db.add(log)
db.commit()
```

## Things to Remember (Frontend)

- **No i18n** - Non-internationalized version
- **Type safety** - Use `@/` path aliases strictly
- **Pinia** - Always use `defineStore` + hooks, not direct imports
- **Mock data** - Development only; replace with real backend

## Things to Remember (Backend)

- **JWT secrets** - Change `SECRET_KEY` in production (use strong random value)
- **CORS config** - Update `CORS_ORIGINS` to match frontend domain
- **Database** - Switch to PostgreSQL for production (not SQLite)
- **Environment** - Never commit `.env` with secrets; use `.env.example`
- **Role permissions** - Auto-assigned based on role in `enums.ROLE_PERMISSIONS`

## Production Checklist

- [ ] Change `SECRET_KEY` to strong random string
- [ ] Set `DEBUG=False` in config
- [ ] Switch `DATABASE_URL` to PostgreSQL
- [ ] Configure `CORS_ORIGINS` to production domain
- [ ] Store secrets in environment variables
- [ ] Run database migrations (Alembic)
- [ ] Enable HTTPS/SSL
- [ ] Set up logging and monitoring
- [ ] Implement rate limiting
- [ ] Configure database backups

## Next Steps

- Implement Document CRUD endpoints
- Implement version control and rollback
- Integrate AI functionality
- Implement Q&A feature
- Add comprehensive test suite
- Set up CI/CD pipeline
