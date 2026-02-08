from pydantic import BaseModel, EmailStr, HttpUrl, Field, validator, model_validator
from typing import Optional
from datetime import datetime, timezone

# --- 1. Shared / Base Schemas ---

class UserBase(BaseModel):
    email: EmailStr

class UrlBase(BaseModel):
    original_url: HttpUrl

# --- 2. Input Schemas (Requests) ---

class UserCreate(UserBase):
    name : str
    password: str = Field(..., min_length=8, description="Must be at least 8 chars")

class UserLogin(UserBase):
    password: str

class UrlCreate(UrlBase):
    custom_alias: Optional[str] = Field(None, max_length=20, min_length=3)
    pin : Optional[int] = Field(None, ge=1000, le=9999)
    expiry_date : Optional[datetime] = Field(None)
    @validator('custom_alias')
    def validate_alias(cls, v):
        if v and not v.isalnum():
            raise ValueError('Alias must be alphanumeric')
        return v
    @model_validator(mode='after')
    def validate_expiry(self) -> 'UrlCreate':
        if self.expiry_date:
            # Ensure the date is in the future
            if self.expiry_date <= datetime.now(timezone.utc):
                raise ValueError('expiry_date must be in the future')
        return self

# --- 3. Output Schemas (Responses) ---

class UserResponse(UserBase):
    id: int
    name: Optional[str] = None
    is_deleted: bool
    provider: str
    
    class Config:
        from_attributes = True
        json_encoders = {int: str}

class UrlResponse(UrlBase):
    id: int
    short_code: str
    created_at: datetime
    user_id: int
    pin: Optional[int] = None
    expiry_date: Optional[datetime] = None
        
    class Config:
        from_attributes = True
        json_encoders = {int: str}

# --- 4. Token Schema (For JWT) ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- 5. Analytics Schemas ---

class LocationStats(BaseModel):
    """Nested structure for Location Data"""
    countries: dict[str, int] = {}
    cities: dict[str, int] = {}

class AnalyticsBase(BaseModel):
    """Shared structure for analytics data"""
    total_clicks: int
    browsers: dict[str, int] = {}
    referers: dict[str, int] = {}
    locations: LocationStats = LocationStats()

class LiveAnalytics(AnalyticsBase):
    """Real-time data from Redis"""
    last_updated: datetime

class HourlyData(AnalyticsBase):
    """Historical data from MongoDB"""
    hour: str

class HistoricalAnalytics(BaseModel):
    total_historical_clicks: int
    history: list[HourlyData]