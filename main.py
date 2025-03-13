from symtable import Class

from fastapi import FastAPI , HTTPException , Depends , status
from pydantic import BaseModel
from typing import Annotated
import  models
from database import engine,SessionLocal
from sqlalchemy.orm import Session

from datetime import date, time

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class NoiseCollectionBase(BaseModel):
    userId : str
    longitude : str
    latitude : str
    date: date
    time: time
    max_noise_val: float
    color_band: str

class UserBase(BaseModel):
    user_id : str
    first_name : str
    last_name : str



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

@app.post("/users/",status_code=status.HTTP_201_CREATED, response_model=UserBase)
async def create_user(user:UserBase,db:db_dependency):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    return db_user 
