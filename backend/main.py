from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.api.v1.endpoints import emissions, visualizations, template, scenarios, chatbot  # Import the new scenarios endpoint

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Adjust this based on your needs.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Mount the static directory to serve CSS, JS, and images
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Jinja2 templates directory
templates = Jinja2Templates(directory="app/templates")

# Include the routers for emissions, visualizations, template, and scenarios endpoints
app.include_router(emissions.router, prefix="/v1", tags=["Emissions"])
app.include_router(visualizations.router, prefix="/v1", tags=["Visualizations"])
app.include_router(template.router, prefix="/v1", tags=["Template"])
app.include_router(scenarios.router, prefix="/v1", tags=["Scenarios"])
app.include_router(chatbot.router, prefix="/v1", tags=["Chatbot"])  # Add this line

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
