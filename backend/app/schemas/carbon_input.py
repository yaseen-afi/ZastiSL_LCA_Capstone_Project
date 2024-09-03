from pydantic import BaseModel
from typing import List

class CarbonInputData(BaseModel):
    name: str
    amount: float

class CarbonInput(BaseModel):
    stage: str
    inputs: List[CarbonInputData]

class CarbonFootprintRequest(BaseModel):
    land_area_hectares: float
    inputs: List[CarbonInput]

class ActivityData(BaseModel):
    name: str
    amount: float
    emission_factor: float
    emission: float

class StageCarbonFootprint(BaseModel):
    stage: str
    activity_data: List[ActivityData]
    total_emission: float

class TotalCarbonFootprintResponse(BaseModel):
    stages: List[StageCarbonFootprint]
    total_carbon_footprint: float
