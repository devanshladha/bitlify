from sqlalchemy import Column, Integer, BigInteger, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base) :
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String)
    email = Column(String, unique = True, index = True)
    hashed_password = Column(String)
    is_deleted = Column(Boolean, default = False)
    provider = Column(String, default = 'local')
    urls = relationship("Url", back_populates = "owner")


class Url(Base):
    __tablename__ = "urls"

    id = Column(BigInteger, primary_key = True, index = True)
    short_code = Column(String, unique=True, index=True, nullable=False)
    original_url = Column(String, index = True, nullable = True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    pin = Column(Integer, nullable=True)
    expiry_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default="working") # (working, disable, banned)
    note = Column(String, default="")

    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="urls")
    # more = relationship("Features", back_populates="origin")

# class Features(Base):
#     __tablename__ = "features"

#     url_id = Column(BigInteger, ForeignKey("urls.id"), primary_key = True, index = True)
#     pin = Column(Integer)
#     expiry_date = Column
#     origin = relationship("Url", back_populates="more")