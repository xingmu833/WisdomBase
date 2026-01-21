from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    """用户模型"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    nickname = Column(String(50), nullable=False)
    avatar = Column(String(255), default="https://avatars.githubusercontent.com/u/44761321")
    roles = Column(String(100), nullable=False)  # JSON格式存储，如 "admin" 或 "editor"
    permissions = Column(Text, nullable=False)  # JSON格式存储权限列表
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)
    
    # 关系
    documents = relationship("Document", back_populates="author", cascade="all, delete-orphan")
    operation_logs = relationship("OperationLog", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, roles={self.roles})>"


class Document(Base):
    """文档模型"""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_published = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关系
    author = relationship("User", back_populates="documents")
    versions = relationship("DocumentVersion", back_populates="document", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Document(id={self.id}, title={self.title}, author_id={self.author_id})>"


class DocumentVersion(Base):
    """文档版本模型"""
    __tablename__ = "document_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 关系
    document = relationship("Document", back_populates="versions")
    
    class Config:
        indexes = [
            ("document_id", "version_number"),
        ]
    
    def __repr__(self):
        return f"<DocumentVersion(id={self.id}, document_id={self.document_id}, version={self.version_number})>"


class OperationLog(Base):
    """操作日志模型"""
    __tablename__ = "operation_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(50), nullable=False)  # CREATE, READ, UPDATE, DELETE, LOGIN等
    resource_type = Column(String(50), nullable=False)  # user, document, system等
    resource_id = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ip_address = Column(String(50), nullable=True)
    
    # 关系
    user = relationship("User", back_populates="operation_logs")
    
    def __repr__(self):
        return f"<OperationLog(id={self.id}, user_id={self.user_id}, action={self.action})>"
