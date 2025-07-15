from typing import List

from pydantic import BaseModel, validator

class Flat(BaseModel):
    flat_name: str
    city: str
    street: str
    street_number: str
    air_conditioning: str
    area: int
    year_built: int
    rent_price: int
    date_available: str
    img_upload: List[str]
    owner: str



