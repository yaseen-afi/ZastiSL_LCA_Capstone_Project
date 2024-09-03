from fastapi import APIRouter, HTTPException
from typing import List
from ....schemas.response_models import EmissionFactor  # Adjust import path
from ....db.session import template_collection  # Adjust import path
from ....schemas.template_schema import Template,RawMaterial,Stage 
from bson import ObjectId

router = APIRouter()

@router.get("/template/{product_type}", response_model=Template)
async def get_template(product_type: str):
    template = await template_collection.find_one({"productType": product_type})
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Convert MongoDB ObjectId to string if needed
    template['_id'] = str(template['_id'])
    
    # Convert MongoDB document to Template model
    return Template(
        product_type=template['productType'],
        raw_material=[
            RawMaterial(
                process=material['Process'],
                amount=material['Amount'],
                unit=material['Unit'],
                basis=material['Basis']
            ) for material in template['rawMaterial']
        ],
        transportation=[
            Stage(
                process=stage['Process'],
                amount=stage['Amount'],
                unit=stage['Unit'],
                basis=stage['Basis']
            ) for stage in template['transportation']
        ],
        manufacturing=[
            Stage(
                process=stage['Process'],
                amount=stage['Amount'],
                unit=stage['Unit'],
                basis=stage['Basis']
            ) for stage in template['manufacturing']
        ]
    )




#@router.post("/emissions", response_model=List[EmissionFactor])
#async def calculate_carbon_footprint(emission_factors: List[EmissionFactor]):
#    try:
#        for factor in emission_factors:
#            updated_data = {
#                "name": factor.name,
#                "unit": factor.unit,
#                "value": factor.value,
#                "source": factor.source
#            }
#            result = await emission_factors_collection.update_one(
#                {"_id": ObjectId(factor.id)},
#                {"$set": updated_data}
#            )
#            if result.matched_count == 0:
#                raise HTTPException(status_code=404, detail=f"Emission factor with id {factor.id} not found.")
#        return emission_factors
#    except Exception as e:
#        raise HTTPException(status_code=500, detail=str(e))
    