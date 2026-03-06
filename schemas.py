from pydantic import BaseModel, EmailStr

class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Response (BaseModel):
    id: int
    is_active: bool

    class Config:
        from_attributes = True