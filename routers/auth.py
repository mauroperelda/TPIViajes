from passlib.context import CryptContext
from schemas.token import Token, TokenData
from config.database import get_db
from typing import List
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from Security import auth
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse, RedirectResponse
import shutil
import os

auth_router = APIRouter()

# ================================
# Autenticación
# ================================
@auth_router.post("/autenticacion", response_model=Token, tags=["Autenticacion"])
async def Login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"})
    if auth.verify_password(form_data.password, user.password):
        access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.CreateAccessToken(data={"sub": user.email}, expires_delta=access_token_expires)
        #return {"access_token": access_token, "token_type": "bearer"}
        response = RedirectResponse(url="/dashboard", status_code = status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return response
