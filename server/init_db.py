"""
初始化脚本 - 创建默认用户
运行方式: python init_db.py
"""

from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User
from security import hash_password
import json
from enums import ROLE_PERMISSIONS, RoleEnum

# 创建所有表
Base.metadata.create_all(bind=engine)


def init_db():
    """初始化数据库并创建默认用户"""
    db = SessionLocal()
    
    try:
        # 检查是否已有用户
        existing_user = db.query(User).filter(User.username == "admin").first()
        if existing_user:
            print("✓ Admin user already exists, skipping initialization")
            return
        
        # 创建三个默认用户
        users_data = [
            {
                "username": "admin",
                "password": "admin123",
                "email": "admin@wisdombase.com",
                "nickname": "小铭",
                "roles": [RoleEnum.ADMIN],
                "avatar": "https://avatars.githubusercontent.com/u/44761321"
            },
            {
                "username": "editor",
                "password": "editor123",
                "email": "editor@wisdombase.com",
                "nickname": "编辑员",
                "roles": [RoleEnum.EDITOR],
                "avatar": "https://avatars.githubusercontent.com/u/52823142"
            },
            {
                "username": "viewer",
                "password": "viewer123",
                "email": "viewer@wisdombase.com",
                "nickname": "查看者",
                "roles": [RoleEnum.VIEWER],
                "avatar": "https://avatars.githubusercontent.com/u/44761321"
            }
        ]
        
        for user_data in users_data:
            roles = [role.value for role in user_data["roles"]]
            permissions = []
            for role in roles:
                if role in ROLE_PERMISSIONS:
                    permissions.extend([p.value for p in ROLE_PERMISSIONS[role]])
            
            user = User(
                username=user_data["username"],
                password=hash_password(user_data["password"]),
                email=user_data["email"],
                nickname=user_data["nickname"],
                roles=json.dumps(roles),
                permissions=json.dumps(list(set(permissions))),
                avatar=user_data["avatar"],
                is_active=True
            )
            db.add(user)
            print(f"✓ Created {user_data['nickname']} ({user_data['username']})")
        
        db.commit()
        print("\n✓ Database initialization completed successfully!")
        print("\nDefault credentials:")
        print("  Admin    | admin    | admin123")
        print("  Editor   | editor   | editor123")
        print("  Viewer   | viewer   | viewer123")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error during initialization: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 50)
    print("WisdomBase API - Database Initialization")
    print("=" * 50)
    init_db()
