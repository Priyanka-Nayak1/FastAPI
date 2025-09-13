from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# User model for registration
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, example="john_doe")
    email: EmailStr = Field(..., example="john@example.com")
    password: str = Field(..., min_length=6, example="strongpassword")


# User model for login
class UserLogin(BaseModel):
    username: str = Field(..., example="john_doe")
    password: str = Field(..., example="strongpassword")


# User model stored in DB (with hashed password)
class UserInDB(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    

# Token response
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Payload inside JWT
class TokenData(BaseModel):
    username: Optional[str] = None
