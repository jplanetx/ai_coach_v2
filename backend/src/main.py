import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import Settings
from .api.tasks import router as tasks_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    logger.info("Starting AI Coach API...")
    
    app = FastAPI(title="AI Coach API")
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://localhost:3001",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(tasks_router)

    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "services": {
                "notion": "connected",
                "openai": "ready"
            }
        }

    return app

app = create_app()