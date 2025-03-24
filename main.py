from symtable import Class

from fastapi import FastAPI , HTTPException , Depends , status
from pydantic import BaseModel
from typing import Annotated, List
import  models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from fastapi import Query
from sqlalchemy.sql import func
from typing import List, Dict

from typing import Optional

from datetime import date, time ,datetime
app = FastAPI()
models.Base.metadata.create_all(bind=engine)
from fastapi.middleware.cors import CORSMiddleware

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)


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
    try:
        today = date.today()
        current_date = today.strftime("%d-%m-%Y")
        curremt_time = datetime.now().strftime("%H:%M:%S")
        color_band = "Green"

        if requestSchema.max_noise_val > 80:
            color_band = "Red"
        elif 20 <= requestSchema.max_noise_val <= 80:
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

    except Exception as e:
        db.rollback()  # Rollback in case of any error
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")



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

@app.get("/noise/all", status_code=status.HTTP_200_OK,response_model=List[NoiseCollectionBase])
async def getAllData(db: db_dependency):
    results = db.query(models.NoiseCollection).all()
    return results


@app.get("/noise/leaderboard", status_code=status.HTTP_200_OK)
async def get_leader_board_details(
    db: db_dependency,
    longitude: Optional[str] = Query(None),
    latitude: Optional[str] = Query(None),
    city: Optional[str] = Query(None) 
):
    if (longitude is None and latitude is not None) or (longitude is not None and latitude is None):
        raise HTTPException(status_code=400, detail="You must provide both latitude and longitude")

    query = (
        db.query(
            models.NoiseCollection.user_id,
            func.count(models.NoiseCollection.user_id).label("report_count"),
            func.sum(models.NoiseCollection.max_noise_val).label("total_dB_collected")
        )
        .group_by(models.NoiseCollection.user_id)
        .order_by(func.count(models.NoiseCollection.user_id).desc())  # Sort by most reports
    )

    if longitude and latitude:
        query = query.filter(models.NoiseCollection.longitude == longitude, models.NoiseCollection.latitude == latitude)
    
    results = query.all()

    # Assign badges based on thresholds
    def assign_badge(report_count, total_dB):
        if report_count >= 5:
            return "Noise Hero"
        elif report_count >= 3:
            return "Silent Guardian"
        elif report_count >= 1:
            return "Noise Rookie"
        
        if total_dB > 50000:
            return "Decibel Master"
        elif total_dB > 10000:
            return "Echo Warrior"
        
        return "Newcomer"

    leaderboard = []
    for user_id, report_count, total_dB in results:
        leaderboard.append({
            "user_id": user_id,
            "report_count": report_count,
            "total_dB_collected": float(total_dB) if total_dB else 0,
            "badge": assign_badge(report_count, total_dB)
        })

    return leaderboard



