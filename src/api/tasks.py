from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from ..services.notion_client import NotionClient
from ..services.task_intelligence import TaskIntelligenceService
from ..core.config import Settings
import logging

router = APIRouter()
settings = Settings()
notion_client = NotionClient(settings)
task_service = TaskIntelligenceService(
    notion_settings=settings.notion,
    openai_settings=settings.openai
)

logger = logging.getLogger(__name__)

@router.get("/api/tasks")
async def get_tasks() -> List[Dict[str, Any]]:
    """Fetch all tasks from Notion with their properties."""
    try:
        logger.info("Attempting to fetch tasks from Notion...")
        tasks = await notion_client.get_tasks()
        logger.info(f"Successfully fetched {len(tasks)} tasks")
        return tasks
    except Exception as e:
        logger.error(f"Error fetching tasks: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/api/tasks/{task_id}/properties")
async def update_task_properties(task_id: str, properties: Dict[str, Any]):
    """Update task properties in Notion."""
    try:
        await notion_client.update_task_properties(task_id, properties)
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error updating task: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/tasks/{task_id}/analyze")
async def analyze_task(task_id: str):
    """Get AI recommendations for task properties."""
    try:
        task = await notion_client.client.pages.retrieve(page_id=task_id)
        task_title = task['properties']['Name']['title'][0]['text']['content']
        
        analysis = await task_service.analyze_task(task_title)
        return analysis
    except Exception as e:
        logger.error(f"Error analyzing task: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))