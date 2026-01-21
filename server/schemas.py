from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# ===== 认证相关 =====
class LoginRequest(BaseModel):
    """登录请求"""
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=6)


class LoginResponse(BaseModel):
    """登录响应"""
    success: bool
    data: Optional[dict] = None
    message: str = ""
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {
                    "avatar": "https://avatars.githubusercontent.com/u/44761321",
                    "username": "admin",
                    "nickname": "小铭",
                    "roles": ["admin"],
                    "permissions": ["*:*:*"],
                    "accessToken": "eyJhbGciOiJIUzUxMiJ9.admin",
                    "refreshToken": "eyJhbGciOiJIUzUxMiJ9.adminRefresh",
                    "expires": "2030/10/30 00:00:00"
                },
                "message": ""
            }
        }


class RefreshTokenRequest(BaseModel):
    """刷新token请求"""
    refreshToken: str


class RefreshTokenResponse(BaseModel):
    """刷新token响应"""
    success: bool
    data: Optional[dict] = None
    message: str = ""


# ===== 用户相关 =====
class UserCreate(BaseModel):
    """创建用户请求"""
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=6)
    email: EmailStr
    nickname: str = Field(..., min_length=1, max_length=50)
    roles: List[str] = ["viewer"]  # 默认为viewer


class UserUpdate(BaseModel):
    """更新用户请求"""
    email: Optional[EmailStr] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    roles: Optional[List[str]] = None


class UserResponse(BaseModel):
    """用户响应"""
    id: int
    username: str
    email: str
    nickname: str
    avatar: str
    roles: List[str]
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """用户列表响应"""
    total: int
    items: List[UserResponse]


# ===== 文档相关 =====
class DocumentCreate(BaseModel):
    """创建文档请求"""
    title: str = Field(..., min_length=1, max_length=255)
    content: str = ""
    is_published: bool = False


class DocumentUpdate(BaseModel):
    """更新文档请求"""
    title: Optional[str] = None
    content: Optional[str] = None
    is_published: Optional[bool] = None


class DocumentResponse(BaseModel):
    """文档响应"""
    id: int
    title: str
    content: str
    author_id: int
    is_published: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    """文档列表响应"""
    total: int
    items: List[DocumentResponse]


# ===== 操作日志相关 =====
class OperationLogResponse(BaseModel):
    """操作日志响应"""
    id: int
    user_id: int
    action: str
    resource_type: str
    resource_id: Optional[int]
    description: Optional[str]
    created_at: datetime
    ip_address: Optional[str]
    
    class Config:
        from_attributes = True


class OperationLogListResponse(BaseModel):
    """操作日志列表响应"""
    total: int
    items: List[OperationLogResponse]


# ===== 通用响应 =====
class ApiResponse(BaseModel):
    """通用API响应"""
    success: bool
    data: Optional[dict] = None
    message: str = ""
