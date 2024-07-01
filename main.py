from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.UserDestinos import destinos_router
from routers.UserPaquetes import paquetes_router
from routers.UserReservas import reservas_router
from routers.UserUsuarios import usuarios_router
from routers.auth import auth_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from Security import auth
from fastapi import APIRouter, Depends, HTTPException, status, Request
from schemas.UserSchema import User
from schemas.token import Token, TokenData
from models.Usuarios import Usuarios as UsuariosModel

app = FastAPI()
app.title = "Viajes"
app.version = "0.0.1"

# Montar la carpeta static para servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar Jinja2Templates
templates = Jinja2Templates(directory="Templates")

@app.get("/", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def read_register(request: Request):
    return templates.TemplateResponse("pages-register.html", {"request": request})

@app.get("/layout", response_class=HTMLResponse)
async def read_layout(request: Request):
    return templates.TemplateResponse("Layout.html", {"request": request})

@app.get("/destinos", response_class=HTMLResponse)
async def read_destinos(request: Request, current_user: UsuariosModel = Depends(auth.GetCurrentUser)):
    return templates.TemplateResponse("destinos.html", {"request": request, "user": current_user})

@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard(request : Request, current_user: UsuariosModel = Depends(auth.GetCurrentUser)):
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": current_user})

@app.get("/paquetes", response_class=HTMLResponse)
async def read_dashboard(request : Request):
    return templates.TemplateResponse("paquetes.html", {"request": request})

@app.get("/reservas_activas", response_class=HTMLResponse)
async def read_dashboard(request : Request):
    return templates.TemplateResponse("reservas_activas.html", {"request": request})

app.add_middleware(ErrorHandler)
## Acá con los CORS (Cross-Origin Resource Sharing)
## defino todos los origenes que van a poder utitlizar/consultar el backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], ##habilito el back para cualquier dominio que quiera consultar
    allow_credentials=True,
    allow_methods=["*"],##habilito todos los métodos HTTP( GET, POST, PUT, HEAD, OPTION, etc)
    allow_headers=["*"],##habilito todos los headers que se puedan enviar desde un navegador.
)
app.include_router(auth_router)
app.include_router(destinos_router, prefix="/api")
app.include_router(paquetes_router, prefix="/api")
app.include_router(reservas_router, prefix="/api")
app.include_router(usuarios_router, prefix="/api")


Base.metadata.create_all(bind=engine)

