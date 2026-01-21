from typing import Optional
from datetime import datetime
import json
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request

from database import get_db
from models import User, OperationLog
from schemas import OperationLogResponse, OperationLogListResponse
from security import get_current_user

router = APIRouter(prefix="/logs", tags=["logs"])


async def require_admin(current_user: User = Depends(get_current_user)):
    """检查管理员权限"""
    roles = json.loads(current_user.roles) if isinstance(current_user.roles, str) else current_user.roles
    if isinstance(roles, str):
        roles = [roles]
    
    if "admin" not in roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can view operation logs"
        )
    return current_user


@router.get("", response_model=OperationLogListResponse)
async def get_operation_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user_id: Optional[int] = None,
    action: Optional[str] = None,
    resource_type: Optional[str] = None,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    获取操作日志（仅管理员）
    
    - **skip**: 跳过的记录数
    - **limit**: 返回的记录数
    - **user_id**: 按用户ID过滤（可选）
    - **action**: 按操作类型过滤（可选）
    - **resource_type**: 按资源类型过滤（可选）
    """
    query = db.query(OperationLog)
    
    if user_id:
        query = query.filter(OperationLog.user_id == user_id)
    if action:
        query = query.filter(OperationLog.action == action)
    if resource_type:
        query = query.filter(OperationLog.resource_type == resource_type)
    
    total = query.count()
    logs = query.order_by(OperationLog.created_at.desc()).offset(skip).limit(limit).all()
    
    return OperationLogListResponse(
        total=total,
        items=[OperationLogResponse.model_validate(log) for log in logs]
    )


@router.get("/{log_id}", response_model=OperationLogResponse)
async def get_operation_log(
    log_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """获取单条操作日志详情（仅管理员）"""
    log = db.query(OperationLog).filter(OperationLog.id == log_id).first()
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operation log not found"
        )
    return OperationLogResponse.model_validate(log)


@router.get("/user/{user_id}")
async def get_user_operation_logs(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """获取特定用户的操作日志（仅管理员）"""
    # 验证用户是否存在
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    total = db.query(OperationLog).filter(OperationLog.user_id == user_id).count()
    logs = db.query(OperationLog).filter(
        OperationLog.user_id == user_id
    ).order_by(OperationLog.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": [OperationLogResponse.model_validate(log) for log in logs]
    }


@router.delete("/{log_id}")
async def delete_operation_log(
    log_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """删除操作日志（仅管理员）"""
    log = db.query(OperationLog).filter(OperationLog.id == log_id).first()
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operation log not found"
        )
    
    db.delete(log)
    db.commit()
    
    return {"success": True, "message": "Operation log deleted successfully"}


@router.delete("")
async def delete_operation_logs_batch(
    log_ids: list[int],
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """批量删除操作日志（仅管理员）"""
    deleted_count = db.query(OperationLog).filter(OperationLog.id.in_(log_ids)).delete()
    db.commit()
    
    return {
        "success": True,
        "message": f"{deleted_count} operation logs deleted successfully",
        "data": {"deleted_count": deleted_count}
    }
