from pydantic import BaseModel
from typing import List

class RawMaterial(BaseModel):
    process: str
    amount: float
    unit: str
    basis: str

class Stage(BaseModel):
    process: str
    amount: float
    unit: str
    basis: str

class Template(BaseModel):
    product_type: str
    raw_material: List[RawMaterial]
    transportation: List[Stage]
    manufacturing: List[Stage]
