from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import settings

client = AsyncIOMotorClient(settings.MONGODB_URI)
database = client[settings.MONGODB_NAME]
OPENAI_API_KEY= settings.OPENAI_API_KEY
emission_factors_collection = database["emission_factors"]
template_collection = database["template"]
scenario_collection = database["Product Systems"]
