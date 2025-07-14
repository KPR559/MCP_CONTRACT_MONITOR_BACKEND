# Modules
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .API.router.router import router as api_router

# Initialize the FastAPI application
app = FastAPI(title="MCP Contract Monitor")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; adjust in production
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Include the API router
app.include_router(api_router)
