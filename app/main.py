from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.responses import JSONResponse
from app.api import rule_routes
from app.services.rule_service import create_rule_service
import logging

# Initialize the FastAPI app
app = FastAPI()

# Include the rule routes 
app.include_router(rule_routes.router)

# Mount static files for the UI
try:
    app.mount("/ui", StaticFiles(directory="ui"), name="ui")
except Exception as e:
    logging.error(f"Error mounting UI: {e}")

# Root endpoint to confirm API is running
@app.get("/")
async def root():
    return {"message": "Rule Engine API is running"}

# Global exception handler for unexpected errors
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logging.error(f"Error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "An internal error occurred. Please try again later."},
    )