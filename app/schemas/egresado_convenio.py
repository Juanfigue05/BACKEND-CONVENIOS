from pydantic import BaseModel, Field
from typing import Optional


class Egresado_convenioBase(BaseModel):
    documento: str = Field(min_length=3, max_length=20)
    num_proceso: str = Field(min_length=3, max_length=20)
    