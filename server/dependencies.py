from fastapi import HTTPException, status, Header, Depends
from typing import Optional
from security import verify_token, get_current_user


async def extract_token(authorization: Optional[str] = Header(None)) -> str:
    """从Authorization请求头中提取token"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return parts[1]


# 修改security中的get_current_user使用新的token提取方式
async def get_current_user_dependency(
    token: str = Depends(extract_token),
    db = None
):
    """获取当前用户（修改后的版本）"""
    from database import get_db
    from security import get_current_user as _get_current_user
    
    db_session = db or next(get_db())
    try:
        return await _get_current_user(token=token, db=db_session)
    finally:
        if db is None:
            db_session.close()
