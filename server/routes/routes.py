from fastapi import APIRouter

router = APIRouter(prefix="/routes", tags=["routes"])


@router.get("/async")
async def get_async_routes():
    """获取异步路由 - 返回动态路由配置"""
    return {
        "success": True,
        "data": [
            # 这里可以根据用户权限动态返回路由
            # 暂时返回空数组，前端会使用本地配置的路由
        ]
    }
