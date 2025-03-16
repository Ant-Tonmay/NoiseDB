from pydantic import BaseModel
from typing import Optional
class NoiseCollectionBase(BaseModel):
    user_id : str
    longitude : str
    latitude : str
    date: str
    time: str
    max_noise_val: float
    color_band: str

class UserBase(BaseModel):
    user_id : str
    first_name : str
    last_name : str

class NoisePostRequestSchema(BaseModel):
    user_id:str
    longitude : str
    latitude : str
    max_noise_val: float

class NoiseFilterSchema(BaseModel):
    user_id: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    longitude: Optional[str] = None
    latitude: Optional[str] = None
    

