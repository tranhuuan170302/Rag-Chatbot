from pydantic import BaseModel

class SignupReq(BaseModel): 
    username: str 
    email: str
    password: str 
    class Config:
        orm_mode = True