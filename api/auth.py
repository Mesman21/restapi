from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from services.auth_service import (
    verify_password, get_password_hash, create_access_token, 
    create_refresh_token, SECRET_KEY, ALGORITHM
)
from schemas.auth import Token, UserCreate
from database import get_users_col
import jwt

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(user: UserCreate):
    users_collection = get_users_col()
    existing_user = await users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    await users_collection.insert_one({"username": user.username, "password": hashed_password})
    return {"msg": "User created successfully"}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    users_collection = get_users_col()
    user = await users_collection.find_one({"username": form_data.username})
    
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    

    return {
        "access_token": create_access_token(data={"sub": user["username"]}),
        "refresh_token": create_refresh_token(data={"sub": user["username"]}),
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
async def refresh(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
        
   
    return {
        "access_token": create_access_token(data={"sub": username}),
        "refresh_token": create_refresh_token(data={"sub": username}),
        "token_type": "bearer"
    }