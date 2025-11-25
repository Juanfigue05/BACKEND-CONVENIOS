from pydantic import BaseModel, Field
from typing import Optional


class MunicipioBase(BaseModel):
    id_municipio: int
    nom_municipio: str = Field(min_length=3, max_length=60)