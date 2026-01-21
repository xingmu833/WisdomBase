from datetime import datetime
import json
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Request

from database import get_db
from models import User, OperationLog
from schemas import LoginRequest, LoginResponse, RefreshTokenRequest, RefreshTokenResponse
from security import hash_password, verify_password, create_token, verify_token, get_current_user
from enums import ROLE_PERMISSIONS, RoleEnum

router = APIRouter(prefix="/auth", tags=["auth"])


def get_client_ip(request: Request) -> str:
    """获取客户端IP地址"""
    if x_forwarded_for := request.headers.get("X-Forwarded-For"):
        return x_forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def log_operation(
    db: Session,
    user_id: int,
    action: str,
    resource_type: str = "auth",
    resource_id: Optional[int] = None,
    description: Optional[str] = None,
    ip_address: Optional[str] = None
):
    """记录操作日志"""
    log = OperationLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        description=description,
        ip_address=ip_address
    )
    db.add(log)
    db.commit()


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    用户登录接口
    
    - **username**: 用户名
    - **password**: 密码
    
    返回access_token、refresh_token和用户信息
    """
    # 查询用户
    user = db.query(User).filter(User.username == login_data.username).first()
    
    if not user or not verify_password(login_data.password, user.password):
        ip_address = get_client_ip(request)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive"
        )
    
    # 更新最后登录时间
    user.last_login = datetime.utcnow()
    db.add(user)
    db.commit()
    
    # 记录登录日志
    ip_address = get_client_ip(request)
    log_operation(
        db=db,
        user_id=user.id,
        action="LOGIN",
        resource_type="auth",
        resource_id=user.id,
        description=f"User {user.username} logged in",
        ip_address=ip_address
    )
    
    # 生成tokens
    access_token = create_token(subject=user.id, token_type="access")
    refresh_token = create_token(subject=user.id, token_type="refresh")
    
    # 解析roles和permissions
    roles = json.loads(user.roles) if isinstance(user.roles, str) else user.roles
    if isinstance(roles, str):
        roles = [roles]
    
    permissions = json.loads(user.permissions) if user.permissions else []
    
    # 格式化过期时间（前端期望的格式）
    expires = (datetime.utcnow() + __import__("datetime").timedelta(
        minutes=__import__("config").settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )).strftime("%Y/%m/%d %H:%M:%S")
    
    return LoginResponse(
        success=True,
        data={
            "avatar": user.avatar,
            "username": user.username,
            "nickname": user.nickname,
            "roles": roles,
            "permissions": permissions,
            "accessToken": access_token,
            "refreshToken": refresh_token,
            "expires": expires
        },
        message=""
    )


@router.post("/refresh-token", response_model=RefreshTokenResponse)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    刷新access token
    
    使用refresh_token获取新的access_token
    """
    try:
        payload = verify_token(refresh_data.refreshToken, token_type="refresh")
        user_id = int(payload.get("sub"))
        
        # 检查用户是否存在且活跃
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # 生成新的access token
        new_access_token = create_token(subject=user.id, token_type="access")
        
        # 格式化过期时间
        expires = (datetime.utcnow() + __import__("datetime").timedelta(
            minutes=__import__("config").settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )).strftime("%Y/%m/%d %H:%M:%S")
        
        return RefreshTokenResponse(
            success=True,
            data={
                "accessToken": new_access_token,
                "refreshToken": refresh_data.refreshToken,
                "expires": expires
            },
            message=""
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.post("/logout")
async def logout(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    用户登出接口
    
    记录用户登出日志
    """
    ip_address = get_client_ip(request)
    log_operation(
        db=db,
        user_id=current_user.id,
        action="LOGOUT",
        resource_type="auth",
        resource_id=current_user.id,
        description=f"User {current_user.username} logged out",
        ip_address=ip_address
    )
    
    return {"success": True, "message": "Logout successful"}


@router.get("/me")
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """获取当前用户信息"""
    roles = json.loads(current_user.roles) if isinstance(current_user.roles, str) else current_user.roles
    if isinstance(roles, str):
        roles = [roles]
    
    permissions = json.loads(current_user.permissions) if current_user.permissions else []
    
    return {
        "success": True,
        "data": {
            "id": current_user.id,
            "avatar": current_user.avatar,
            "username": current_user.username,
            "nickname": current_user.nickname,
            "email": current_user.email,
            "roles": roles,
            "permissions": permissions,
            "is_active": current_user.is_active,
            "created_at": current_user.created_at,
            "last_login": current_user.last_login
        },
        "message": ""
    }
