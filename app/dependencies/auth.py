from datetime import datetime, timedelta 
from passlib.context import CryptContext

from fastapi import Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from jose import jwt, JWTError 

from app import settings 
from .database import Session 
from models import User 
from schemas import TokenData 

SECRET_KEY = settings.SECRET_KEY 
ALGORITHM = settings.ALGORITHM 
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 

def verify_password(plain_password : str, hashed_password: str ) -> bool : 
    return pwd_context.verify(plain_password, hashed_password) 

def hash_password(password : str) -> str: 
    return pwd_context.hash(password) 

def authenticate_user(username : str, password : str, db : Session) : 
    user = db.query(User).filter(User.username == username).first() 
    if not user: 
        return False
    if not verify_password(password, user.password_hash): 
        return False 
    return user 

def create_access_token(data : dict, expires_delta: timedelta): 
    to_encode = data.copy() 
    expire = datetime.utcnow() + expires_delta 
    to_encode.update({"exp": expire}) 
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) 
    return encoded_jwt 

async def get_current_user(token : str = Depends(oauth2_scheme), db: Session = Depends(get_db)): 
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
        
        username : str = payload.get("sub") 
        if username is None: 
            raise HTTPException(status_code=401, detail="Invalid authentication credentials") 
        token_data = schemas.TokenData(username=username) 
    except JWTError: 
        raise HTTPException(status_code=401, detail="Invalid authentication credentials") 
    
    user = db.query(User).filter(User.username == username).first() 

    if user is None: 
        raise HTTPException(status_code=404, detail="User not found") 
    return user 

async def authenticate(form_data: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)): 
    user = authenticate_user(form_data.username, form_data.password, db) 
    if not user: 
        raise HTTPException(status_code=401, detail="Incorect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) 
    access_token = create_access_token(
        data = {"sub": user.username }, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}