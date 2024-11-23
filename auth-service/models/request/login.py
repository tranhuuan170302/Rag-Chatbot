from pydantic import BaseModel

class LoginReq(BaseModel): 
    email: str
    password: str 
    class Config:
        orm_mode = True