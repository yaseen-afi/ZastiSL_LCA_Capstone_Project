from pydantic import BaseModel

class EmissionFactor(BaseModel):
    id: str
    name: str
    unit: str
    value: float
    source: str

    class Config:
        json_schema_extra = {
            "example": {
                "Process": "CO2 Emission",
                "unit": "kg",
                "value": 10.0,
                "source": "IPCC"
            }
        }
