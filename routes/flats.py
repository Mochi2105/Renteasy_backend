from fastapi import APIRouter, Form, UploadFile, File
from fastapi.params import Depends
from typing import List

from middleware.auth import get_current_user
from models.user import User
from services.flat_service import create_flat, get_flats, update_flat
from models.flat import Flat

router = APIRouter(prefix="/flats", tags=["flats"])

@router.post("/new_flat")
async def create_new_flat_router(
    flat_name: str = Form(...),
    city: str = Form(...),
    street: str = Form(...),
    street_number: str = Form(...),
    air_conditioning: str = Form(...),
    area: int = Form(...),
    year_built: int = Form(...),
    rent_price: int = Form(...),
    date_available: str = Form(...),
    img_upload: List[UploadFile] = File(...),
    current_user: dict = Depends(get_current_user)
):
    flat_data = Flat(
        flat_name=flat_name,
        city=city,
        street=street,
        street_number=street_number,
        air_conditioning=air_conditioning,
        area=area,
        year_built=year_built,
        rent_price=rent_price,
        date_available=date_available,
        img_upload=[],
        owner=current_user["_id"]
    )
    return await create_flat(flat_data, img_upload)


@router.get('/')
def get_flats_route():
    return get_flats()


@router.put('/{id}')
def update_flat_route(flat: Flat, id:str, current_user: dict = Depends(get_current_user)): #funcion de dependencia-privado
    return update_flat(id, flat)