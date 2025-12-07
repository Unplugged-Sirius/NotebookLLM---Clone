# FastAPI backend exposing endpoints
"""FastAPI server and API endpoints."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import Config

app = FastAPI(title="Learning Helper API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.get("/api/search")
def search(query: str):
    """Search for learning resources."""
    pass

@app.post("/api/resources")
def add_resource(resource: dict):
    """Add a new learning resource."""
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=Config.FASTAPI_HOST, port=Config.FASTAPI_PORT)
