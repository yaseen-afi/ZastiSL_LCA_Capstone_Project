from fastapi import APIRouter, HTTPException
from typing import List
from ....schemas.response_models import EmissionFactor  # Adjust import path
from ....db.session import emission_factors_collection  # Adjust import path
#from ....schemas.carbon_input import CarbonInput, StageCarbonFootprint, TotalCarbonFootprintResponse  # Adjusted import path
from ....schemas.carbon_input import CarbonFootprintRequest, TotalCarbonFootprintResponse, StageCarbonFootprint, ActivityData
from bson import ObjectId

router = APIRouter()

@router.get("/emissions", response_model=List[EmissionFactor])
async def get_emissions():
    try:
        emissions = []
        async for doc in emission_factors_collection.find():
            # Convert ObjectId to string
            doc['_id'] = str(doc['_id'])
            # Convert document to EmissionFactor model
            emission = EmissionFactor(
                id=doc['_id'],
                name=doc.get('name', ''),
                unit=doc.get('unit', ''),
                value=doc.get('value', 0.0),
                source=doc.get('source', '')
            )
            emissions.append(emission)
        return emissions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# @router.post("/calculate-carbon-footprint", response_model=TotalCarbonFootprintResponse)
# async def calculate_carbon_footprint(inputs: List[CarbonInput]):
#     try:
#         stages = []
#         total_carbon_footprint = 0.0

#         for stage_input in inputs:
#             stage_total_emission = 0.0
#             activity_data = []

#             for input_data in stage_input.inputs:
#                 emission_factor = await emission_factors_collection.find_one({"name": input_data.name})
#                 if not emission_factor:
#                     raise HTTPException(status_code=404, detail=f"Emission factor for {input_data.name} not found")
                
#                 emission = input_data.amount * emission_factor['value']
#                 activity_data.append({
#                     "name": input_data.name,
#                     "amount": input_data.amount,
#                     "emission_factor": emission_factor['value'],
#                     "emission": emission
#                 })
#                 stage_total_emission += emission
            
#             stages.append(StageCarbonFootprint(
#                 stage=stage_input.stage,
#                 activity_data=activity_data,
#                 total_emission=stage_total_emission
#             ))
#             total_carbon_footprint += stage_total_emission

#         return TotalCarbonFootprintResponse(stages=stages, total_carbon_footprint=total_carbon_footprint)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


@router.post("/emissions", response_model=List[EmissionFactor])
async def calculate_carbon_footprint(emission_factors: List[EmissionFactor]):
    try:
        for factor in emission_factors:
            updated_data = {
                "name": factor.name,
                "unit": factor.unit,
                "value": factor.value,
                "source": factor.source
            }
            result = await emission_factors_collection.update_one(
                {"_id": ObjectId(factor.id)},
                {"$set": updated_data}
            )
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail=f"Emission factor with id {factor.id} not found.")
        return emission_factors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/calculate-carbon-footprint", response_model=TotalCarbonFootprintResponse)
async def calculate_carbon_footprint(request: CarbonFootprintRequest):
    try:
        stages = []
        total_carbon_footprint = 0.0

        land_area_hectares = request.land_area_hectares

        for stage_input in request.inputs:
            stage_total_emission = 0.0
            activity_data = []

            for input_data in stage_input.inputs:
                emission_factor = await emission_factors_collection.find_one({"name": input_data.name})
                if not emission_factor:
                    raise HTTPException(status_code=404, detail=f"Emission factor for {input_data.name} not found")
                
                emission = input_data.amount * emission_factor['value']
                activity_data.append(ActivityData(
                    name=input_data.name,
                    amount=input_data.amount,
                    emission_factor=emission_factor['value'],
                    emission=emission
                ))
                stage_total_emission += emission

            # Apply the multipliers based on stage
            if stage_input.stage == "Raw Materials":
                stage_total_emission *= land_area_hectares
            elif stage_input.stage == "Manufacturing":
                hemp_milk_production_per_tonne_seeds = 1.5  # Example multiplier, replace with actual value
                seed_production_tonnes_per_ha_year = 1850  # Example multiplier, replace with actual value
                stage_total_emission *= hemp_milk_production_per_tonne_seeds * seed_production_tonnes_per_ha_year * land_area_hectares
            
            stages.append(StageCarbonFootprint(
                stage=stage_input.stage,
                activity_data=activity_data,
                total_emission=stage_total_emission
            ))
            total_carbon_footprint += stage_total_emission

        return TotalCarbonFootprintResponse(stages=stages, total_carbon_footprint=total_carbon_footprint)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))