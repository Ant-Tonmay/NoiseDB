from sqlalchemy import Boolean, Column, Integer, String, Numeric, ForeignKey , Date , Time
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(20), unique=True)
    first_name = Column(String(20))
    last_name = Column(String(20))

    # Relationship to NoiseCollection
    noise_collections = relationship("NoiseCollection", back_populates="user")

class NoiseCollection(Base):
    __tablename__ = "noise"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(20), ForeignKey('users.user_id'))  # Foreign key reference
    longitude = Column(String(10))
    latitude = Column(String(10))
    date = Column(String(10))
    time = Column(String(10))
    max_noise_val = Column(Numeric)
    color_band = Column(String(10))

    # Relationship to User
    user = relationship("User", back_populates="noise_collections")
    
