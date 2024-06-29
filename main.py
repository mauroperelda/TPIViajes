from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.UserDestinos import destinos_router
from routers.UserPaquetes import paquetes_router
from routers.UserReservas import reservas_router
from routers.UserUsuarios import usuarios_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI()
app.title = "Viajes"
app.version = "0.0.1"

# Montar la carpeta static para servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar Jinja2Templates
templates = Jinja2Templates(directory="Templates")

@app.get("/")
async def read_dashboard(request: Request):
    return templates.TemplateResponse("Layout.html", {"request": request})

app.add_middleware(ErrorHandler)
app.include_router(destinos_router)
app.include_router(paquetes_router)
app.include_router(reservas_router)
app.include_router(usuarios_router)


Base.metadata.create_all(bind=engine)

