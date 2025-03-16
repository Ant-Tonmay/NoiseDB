from symtable import Class

from fastapi import FastAPI , HTTPException , Depends , status
from pydantic import BaseModel
from typing import Annotated, List
import  models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from fastapi import Query

from typing import Optional

from datetime import date, time ,datetime
app = FastAPI()
models.Base.metadata.create_all(bind=engine)

from request_schema import UserBase,NoiseCollectionBase,NoisePostRequestSchema,NoiseFilterSchema

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

@app.post("/noise/",status_code=status.HTTP_201_CREATED,response_model=NoiseCollectionBase)
async def create_noise_entry(requestSchema:NoisePostRequestSchema,db:db_dependency):
    today = date.today()
    current_date = today.strftime("%d-%m-%Y")
    curremt_time = datetime.now().strftime("%H:%M:%S")
    color_band="Green"
    if requestSchema.max_noise_val>80 :
        color_band ="Red"
    elif requestSchema.max_noise_val>=20 and requestSchema.max_noise_val <=80:
        color_band = "Yellow"
    noiseDataBase = NoiseCollectionBase(
            user_id=requestSchema.user_id,
            longitude=requestSchema.longitude,
            latitude=requestSchema.latitude,
            date=current_date,
            time=curremt_time,
            color_band=color_band,
            max_noise_val=requestSchema.max_noise_val
        )
    noiseData = models.NoiseCollection(**noiseDataBase.model_dump())
    db.add(noiseData)
    db.commit()
    return noiseDataBase



@app.get("/noise/",status_code=status.HTTP_200_OK,response_model=List[NoiseCollectionBase]
)
async def get_noise_data(
     db:db_dependency,
    user_id: str,
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    longitude: Optional[str] = Query(None),
    latitude: Optional[str] = Query(None),
):
    
    if user_id == None:
        raise HTTPException(status_code=404,detail='user_id not found')
    elif end_date != None and start_date == None:
       raise HTTPException(status_code=404,detail='You must provide start_date if you are providing end_date')
    elif (longitude == None and latitude!=None) or (longitude != None and latitude==None):
        raise HTTPException(status_code=404,detail='You must provide latitude and longitude both')
    
    query = db.query(models.NoiseCollection).filter(models.NoiseCollection.user_id == user_id)

    if start_date:
        query = query.filter(models.NoiseCollection.date >= start_date)
    if end_date:
        query = query.filter(models.NoiseCollection.date <= end_date)
    if longitude:
        query = query.filter(models.NoiseCollection.longitude == longitude)
    if latitude:
        query = query.filter(models.NoiseCollection.latitude == latitude)

    results = query.all()
    return results
