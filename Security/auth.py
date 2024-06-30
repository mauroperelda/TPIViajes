from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, status, Security, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from schemas.token import Token, TokenData
from models.Usuarios import Usuarios as UsuariosModel

# ================================
# Seguridad y Autenticación
# ================================

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para verificar contraseñas
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Función para obtener el hash de una contraseña
def GetPasswordHash(password):
    return pwd_context.hash(password)

def get_user(db, email: str):
    return db.query(UsuariosModel).filter(UsuariosModel.email == email).first()

# Función para crear un token de acceso JWT
def CreateAccessToken(data:dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def GetCurrentUser(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(username=email)
    except jwt.PyJWTError:
        raise credentials_exception
    user = get_user(db, email=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Simulación de una base de datos de usuarios
# fake_users_db = {
#     "mauroperelda": {
#         "username": "mauroperelda",
#         "full_name": "Mauro Perelda",
#         "email": "mauroperelda10@gmail.com",
#         "hashed_password": GetPasswordHash("Maurop10133"),
#         "disabled": False,
#     }
# }

# Función para autenticar usuarios
def authenticate_user(db, email: str, password: str):
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user