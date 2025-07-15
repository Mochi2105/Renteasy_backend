import os
from typing import List

from bson import ObjectId
from fastapi import HTTPException, UploadFile

from database.mongo import db
from models.flat import Flat
from datetime import datetime

import uuid

db_flats = db['flats']

UPLOAD_DIRECTORY = "static/images/flats" #variable   guardar las imagenes

API_URL = "http://localhost:8080/static/images/flats" # consulta la direccion de las imagenes y ver en el navegador

async def create_flat(flat: Flat, upload_files: List[UploadFile]):  #recibo como parametros los archivos

    try:
        new_flat = Flat(
            flat_name= flat.flat_name,
            city= flat.city,
            street= flat.street,
            street_number= flat.street_number,
            air_conditioning= flat.air_conditioning,
            area= flat.area,
            year_built= flat.year_built,
            rent_price= flat.rent_price,
            date_available= flat.date_available,
            img_upload= [],
            owner= flat.owner,

        )

        new_flat["created_at"] = datetime.now()

        result = db_flats.insert_one(new_flat) #insertar un nuevo documento

        result_id = result.inserted_id  #obtengo el id de ese documento

        images_path = [] #variable para las imagenes

        user_upload_directory = os.path.join(UPLOAD_DIRECTORY, flat.owner, str(result_id))
        os.makedirs(user_upload_directory, exist_ok = True)

        for image in upload_files:
            file_extension = image.filename.split(".")[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_location = os.path.join(user_upload_directory, unique_filename)
            with open(file_location, "wb") as file_object:
                file_object.write(await image.file.read())
            images_path.append(f"{API_URL}/{flat.owner}/{result_id}/{unique_filename}")

        db_flats.update_one(
            {"_id": result_id},
            {"$set":{"img_upload": images_path}}
        )

        return {"message": "Flat is successfully published"}

    except AttributeError:
        raise HTTPException(status_code=404, detail="Error inserting flat into the database")
    return {"message": "Flat created successfully"}


def get_flats():
    try:
        results = []

        for item in db_flats.find():
            item['_id'] = str(item['_id'])
            results.append(item)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving flats: {str(e)}")


def update_flat(id:str, flat:Flat):
    try:
        data_flat = flat.model_dump()
        db_flats.update_one({'_id': ObjectId(id)},{'$set': data_flat})
        return {"message": "Flat updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating flat: {str(e)}")