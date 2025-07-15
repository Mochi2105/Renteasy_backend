from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from routes import users, flats

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173", #frontend (Vite, por ejemplo)
    "http://127.0.0.1:5173", # útil en ambos casos
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router)
app.include_router(flats.router)

for route in app.routes:
    print ("Registered route", route.path, "-", route.methods)      # todas las rutas vistas

app.mount("/static/images/", StaticFiles(directory="static/images/"), name="images") #path de las imagenes

