from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, status, Security, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional
from datetime import datetime, timedelta
from passlib.context import CryptContext
import shutil
import os

# Modelo para el token
class Token(BaseModel):
    access_token: str
    token_type: str

# Modelo para el token de datos
class TokenData(BaseModel):
    username: str | None = None