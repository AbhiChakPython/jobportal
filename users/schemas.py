from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserProfileAPISchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    phone_number: Optional[str] = Field(None, min_length=10, max_length=15)
    location: Optional[str] = Field(None, min_length=3, max_length=100)
    experience: Optional[int] = Field(None, ge=0)
    education: Optional[str] = None
    skills: Optional[str] = None
    email: Optional[EmailStr] = None

    class Config:
        from_attributes: True
