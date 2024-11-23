from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from models.data.sqlalchemy_models import Signup, Login
from repository.signup import SignupRepository
from repository.login import LoginRepository
from models.request.signup import SignupReq
from models.request.login import LoginReq
from typing import Annotated, List
from db_config.sqlalchemy_connect import sess_db
from fastapi.security import HTTPBasicCredentials, OAuth2PasswordRequestForm
from security.secure import authenticate, http_basic, get_password_hash, verified_password, create_access_token

from datetime import date, timedelta
router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/signup/add")
def add_signup(req: SignupReq, sess:Session = Depends(sess_db)):
    repo:SignupRepository = SignupRepository(sess)
    signup = Signup(password= req.password, username=req.username, email=req.email)
    result = repo.insert_signup(signup)
    if result == True:
        return signup
    else: 
        return JSONResponse(content={'message':'create signup problem encountered'}, status_code=500)
    
@router.get('/approve/signup')
def signup_approve(email: str, sess:Session = Depends(sess_db)):
    print("hello")
    signuprepo = SignupRepository(sess)
    print(f"Email: {email}")
    result:Signup = signuprepo.get_signup_email(email)
    print(result)
    if result == None:
        return JSONResponse(content={'message':'User not found'}, status_code=401)
    else:
        passphrase = get_password_hash(result.password)
        print(f"pasphrase: {passphrase}")
        login = Login(id=result.id, email=result.email, password=result.password, passphrase=passphrase, approved_date=date.today())
        loginrepo = LoginRepository(sess)
        success = loginrepo.insert_login(login)
        if success == False: 
            return JSONResponse(content={'message':'create login problem encountered'}, status_code=500)
        else:
            return login

@router.get("/login")
def login(credentials: HTTPBasicCredentials = Depends(http_basic), sess:Session = Depends(sess_db)):    
    loginrepo = LoginRepository(sess)
    account = loginrepo.get_all_login_username(credentials.username)    
    if authenticate(credentials, account) and not account == None: 
        data = {'username': account.email, 'password': account.password}
        access_token = create_access_token(data, expires_after=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))       
        return JSONResponse(content={'access_token': access_token})
    else:
        raise HTTPException(status_code=400, detail="Incorrect credentials")
