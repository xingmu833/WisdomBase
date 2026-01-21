from enum import Enum


class RoleEnum(str, Enum):
    """用户角色枚举"""
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


class PermissionEnum(str, Enum):
    """权限枚举"""
    # 管理员权限
    ADMIN_FULL = "*:*:*"
    
    # 文档权限
    DOC_CREATE = "document:create"
    DOC_READ = "document:read"
    DOC_UPDATE = "document:update"
    DOC_DELETE = "document:delete"
    
    # 用户管理权限
    USER_MANAGE = "user:manage"
    USER_READ = "user:read"
    
    # 日志权限
    LOG_VIEW = "log:view"
    
    # 版本控制权限
    VERSION_ROLLBACK = "version:rollback"
    
    # AI功能权限
    AI_CALL = "ai:call"
    
    # 问答功能权限
    QA_USE = "qa:use"


# 角色与权限映射
ROLE_PERMISSIONS = {
    RoleEnum.ADMIN: [
        PermissionEnum.ADMIN_FULL,
        PermissionEnum.DOC_CREATE,
        PermissionEnum.DOC_READ,
        PermissionEnum.DOC_UPDATE,
        PermissionEnum.DOC_DELETE,
        PermissionEnum.USER_MANAGE,
        PermissionEnum.USER_READ,
        PermissionEnum.LOG_VIEW,
        PermissionEnum.VERSION_ROLLBACK,
        PermissionEnum.AI_CALL,
        PermissionEnum.QA_USE,
    ],
    RoleEnum.EDITOR: [
        PermissionEnum.DOC_CREATE,
        PermissionEnum.DOC_READ,
        PermissionEnum.DOC_UPDATE,
        PermissionEnum.VERSION_ROLLBACK,
        PermissionEnum.AI_CALL,
    ],
    RoleEnum.VIEWER: [
        PermissionEnum.DOC_READ,
        PermissionEnum.QA_USE,
    ]
}
