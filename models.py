from sqlalchemy import Column,Integer,String,Boolean,DateTime
from database import Base
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID

class User(Base):

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)

    name = Column(String)
    email = Column(String,unique=True,index=True)
    hashed_password = Column(String)
    current_session_id = Column(String, nullable=True,unique=True)
    is_active = Column(Boolean,default=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

