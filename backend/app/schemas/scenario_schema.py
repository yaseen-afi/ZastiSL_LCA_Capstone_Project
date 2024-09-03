from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class EmissionFactor(BaseModel):
    process: str
    basis: str
    value: float
    source: str

class StageProcess(BaseModel):
    process: str
    amount: float
    unit: str
    basis: str

class ScenarioStage(BaseModel):
    stage: str
    processes: Optional[List[StageProcess]] = None  # Make processes optional

class FarmLandArea(BaseModel):
    value: float
    unit: str

class Scenario(BaseModel):
    product_system_name: str
    created_date: str
    farm_land_area: FarmLandArea
    product_type: str
    comments: str
    stages: Optional[List[ScenarioStage]] = None  # Make stages optional
    emission_factors: Optional[List[EmissionFactor]] = None  # Make emission_factors optional

    class Config:
        schema_extra = {
            "example": {
                "product_system_name": "Hemp Energy Product 1",
                "created_date": "2024-08-30",
                "farm_land_area": {
                    "value": 100,
                    "unit": "hectares"
                },
                "product_type": "hempEnergy",
                "comments": "Sample comments here.",
                "stages": [
                    {
                        "stage": "Raw Material",
                        "processes": [
                            {
                                "process": "Straw Production",
                                "amount": 1260,
                                "unit": "tonnes",
                                "basis": "/ha.year"
                            },
                            {
                                "process": "Fertilizer Application: Urea-N",
                                "amount": 325,
                                "unit": "tonnes",
                                "basis": "/ha.year"
                            }
                        ]
                    }
                ],
                "emission_factors": [
                    {
                        "process": "Fertilizer Production Urea-N",
                        "basis": "per kg",
                        "value": 3.344621677,
                        "source": "(10 a) IPCC 2018"
                    }
                ]
            }
        }

class ScenarioInDB(Scenario):
    id: str  # MongoDB document ID
