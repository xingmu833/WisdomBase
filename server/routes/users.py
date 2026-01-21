from typing import Optional
import json
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Query

from database import get_db
from models import User, OperationLog
from schemas import UserResponse, UserListResponse, UserCreate, UserUpdate
from security import hash_password, get_current_user
from enums import ROLE_PERMISSIONS

router = APIRouter(prefix="/users", tags=["users"])


async def require_admin(current_user: User = Depends(get_current_user)):
    """检查管理员权限"""
    roles = json.loads(current_user.roles) if isinstance(current_user.roles, str) else current_user.roles
    if isinstance(roles, str):
        roles = [roles]
    
    if "admin" not in roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access this resource"
        )
    return current_user


@router.get("", response_model=UserListResponse)
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    获取用户列表（仅管理员）
    
    - **skip**: 跳过的记录数
    - **limit**: 返回的记录数
    """
    total = db.query(User).count()
    users = db.query(User).offset(skip).limit(limit).all()
    
    return UserListResponse(
        total=total,
        items=[UserResponse.model_validate(user) for user in users]
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """获取用户详情（仅管理员）"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse.model_validate(user)


@router.post("", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    创建新用户（仅管理员）
    
    - **username**: 用户名（唯一）
    - **password**: 密码
    - **email**: 邮箱（唯一）
    - **nickname**: 昵称
    - **roles**: 角色列表
    """
    # 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    # 检查邮箱是否已存在
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
    # 获取权限
    permissions = []
    for role in user_data.roles:
        if role.lower() in ROLE_PERMISSIONS:
            permissions.extend(ROLE_PERMISSIONS[role.lower()])
    
    # 创建用户
    new_user = User(
        username=user_data.username,
        password=hash_password(user_data.password),
        email=user_data.email,
        nickname=user_data.nickname,
        roles=json.dumps(user_data.roles),
        permissions=json.dumps(list(set(permissions))),  # 去重
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # 记录操作日志
    log = OperationLog(
        user_id=current_user.id,
        action="CREATE",
        resource_type="user",
        resource_id=new_user.id,
        description=f"Created user {new_user.username}"
    )
    db.add(log)
    db.commit()
    
    return UserResponse.model_validate(new_user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    更新用户信息（仅管理员）
    
    - **email**: 邮箱
    - **nickname**: 昵称
    - **avatar**: 头像URL
    - **roles**: 角色列表
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # 检查邮箱是否已被其他用户使用
    if user_data.email and user_data.email != user.email:
        existing_email = db.query(User).filter(
            User.email == user_data.email,
            User.id != user_id
        ).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
    
    # 更新字段
    if user_data.email:
        user.email = user_data.email
    if user_data.nickname:
        user.nickname = user_data.nickname
    if user_data.avatar:
        user.avatar = user_data.avatar
    if user_data.roles:
        permissions = []
        for role in user_data.roles:
            if role.lower() in ROLE_PERMISSIONS:
                permissions.extend(ROLE_PERMISSIONS[role.lower()])
        user.roles = json.dumps(user_data.roles)
        user.permissions = json.dumps(list(set(permissions)))
    
    user.updated_at = datetime.utcnow()
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # 记录操作日志
    log = OperationLog(
        user_id=current_user.id,
        action="UPDATE",
        resource_type="user",
        resource_id=user_id,
        description=f"Updated user {user.username}"
    )
    db.add(log)
    db.commit()
    
    return UserResponse.model_validate(user)


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """删除用户（仅管理员，不能删除自己）"""
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete yourself"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    username = user.username
    db.delete(user)
    db.commit()
    
    # 记录操作日志
    log = OperationLog(
        user_id=current_user.id,
        action="DELETE",
        resource_type="user",
        resource_id=user_id,
        description=f"Deleted user {username}"
    )
    db.add(log)
    db.commit()
    
    return {"success": True, "message": f"User {username} deleted successfully"}


@router.put("/{user_id}/status")
async def toggle_user_status(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """切换用户激活状态（仅管理员）"""
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change your own status"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = not user.is_active
    db.add(user)
    db.commit()
    
    # 记录操作日志
    log = OperationLog(
        user_id=current_user.id,
        action="UPDATE",
        resource_type="user",
        resource_id=user_id,
        description=f"{'Activated' if user.is_active else 'Deactivated'} user {user.username}"
    )
    db.add(log)
    db.commit()
    
    return {
        "success": True,
        "data": {"is_active": user.is_active},
        "message": f"User status changed to {'active' if user.is_active else 'inactive'}"
    }
