from fastapi import APIRouter, HTTPException, status
from typing import List
from ....schemas.scenario_schema import Scenario, ScenarioInDB  # Adjust import paths
from ....db.session import scenario_collection  # Adjust import path
from bson import ObjectId

router = APIRouter()

@router.post("/scenarios", response_model=ScenarioInDB, status_code=status.HTTP_201_CREATED)
async def create_scenario(scenario: Scenario):
    # Convert the Pydantic model to a dictionary
    scenario_dict = scenario.dict()

    # Insert the scenario into the MongoDB collection
    result = await scenario_collection.insert_one(scenario_dict)

    # Retrieve the inserted document
    inserted_scenario = await scenario_collection.find_one({"_id": result.inserted_id})

    if not inserted_scenario:
        raise HTTPException(status_code=404, detail="Scenario not saved properly")
    
    # Convert MongoDB ObjectId to string for returning the scenario with an ID
    inserted_scenario['id'] = str(inserted_scenario['_id'])
    inserted_scenario.pop('_id')  # Remove the MongoDB-specific '_id' key

    return ScenarioInDB(**inserted_scenario)



@router.get("/scenarios", response_model=List[ScenarioInDB])
async def get_scenarios():
    scenarios_cursor = scenario_collection.find({}, {
        "product_system_name": 1,
        "created_date": 1,
        "farm_land_area": 1,
        "product_type": 1,
        "comments": 1,
        "stages": 1,
        "emission_factors": 1
    })

    scenarios = await scenarios_cursor.to_list(length=None)

    if not scenarios:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No scenarios found")

    # Ensure all required fields are present
    for scenario in scenarios:
        scenario['id'] = str(scenario['_id'])
        scenario.pop('_id')  # Remove the MongoDB-specific '_id' key

        # Provide defaults for missing fields
        if 'stages' not in scenario:
            scenario['stages'] = []
        if 'emission_factors' not in scenario:
            scenario['emission_factors'] = []

    return [ScenarioInDB(**scenario) for scenario in scenarios]