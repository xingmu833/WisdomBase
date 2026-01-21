from datetime import datetime, timedelta, timezone
from typing import Optional
import json

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from config import settings
from database import get_db
from models import User
from enums import ROLE_PERMISSIONS

# 密码加密上下文 - 使用 argon2（更安全，无长度限制）
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    """对密码进行哈希"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def create_token(
    subject: str,
    token_type: str = "access",
    expires_delta: Optional[timedelta] = None
) -> str:
    """创建JWT Token
    
    Args:
        subject: 通常是用户ID
        token_type: token类型 (access/refresh)
        expires_delta: 过期时间间隔
    """
    if expires_delta is None:
        if token_type == "access":
            expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        else:
            expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": token_type
    }
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> dict:
    """验证JWT Token
    
    Args:
        token: 要验证的token
        token_type: 期望的token类型
        
    Returns:
        token的payload字典
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        token_type_in_token: str = payload.get("type")
        
        if user_id is None or token_type_in_token != token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


async def get_current_user(
    token: str = None,
    db: Session = Depends(get_db)
) -> User:
    """从token中获取当前用户
    
    Args:
        token: 从请求头中提取的access token
        db: 数据库会话
        
    Returns:
        当前用户对象
    """
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No token provided"
        )
    
    payload = verify_token(token, token_type="access")
    user_id: int = int(payload.get("sub"))
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    return user


async def get_user_permissions(user: User = Depends(get_current_user)) -> list:
    """获取用户权限列表"""
    try:
        permissions = json.loads(user.permissions)
        if isinstance(permissions, list):
            return permissions
    except (json.JSONDecodeError, TypeError):
        pass
    return []


def check_permission(required_permission: str):
    """权限检查依赖"""
    async def permission_checker(
        current_user: User = Depends(get_current_user),
        permissions: list = Depends(get_user_permissions)
    ):
        # 如果有admin权限，直接通过
        if "*:*:*" in permissions or "permission:btn:*" in permissions:
            return True
        
        if required_permission not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return True
    
    return permission_checker
