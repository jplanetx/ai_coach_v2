from typing import Dict, Any, Optional, List
from notion_client import Client, AsyncClient
import logging
from ..core.config import Settings

logger = logging.getLogger(__name__)

def get_text_content(title_prop):
    """Safely get text content from a title property."""
    try:
        if not title_prop or not isinstance(title_prop, dict):
            return ""
        title_array = title_prop.get("title", [])
        if not title_array:
            return ""
        first_title = title_array[0]
        if not first_title:
            return ""
        text_content = first_title.get("text", {}).get("content", "")
        return text_content
    except Exception as e:
        logger.error(f"Error extracting text content: {str(e)}")
        return ""

def get_select_value(prop):
    """Safely get select value from a property."""
    try:
        if not prop or not isinstance(prop, dict):
            return "Medium"
        select_data = prop.get("select", {})
        if not select_data:
            return "Medium"
        return select_data.get("name", "Medium")
    except Exception as e:
        logger.error(f"Error extracting select value: {str(e)}")
        return "Medium"

def get_status_value(prop):
    """Safely get status value from a property."""
    try:
        if not prop or not isinstance(prop, dict):
            return "To-do"
        status_data = prop.get("status", {})
        if not status_data:
            return "To-do"
        return status_data.get("name", "To-do")
    except Exception as e:
        logger.error(f"Error extracting status value: {str(e)}")
        return "To-do"

class NotionClient:
    def __init__(self, settings: Settings):
        self.client = AsyncClient(auth=settings.NOTION_API_KEY)
        self.tasks_database_id = settings.NOTION_TASKS_DATABASE_ID
        logger.info(f"NotionClient initialized with tasks database ID: {self.tasks_database_id}")
    
    async def get_tasks(self) -> List[Dict[str, Any]]:
        """Fetch all tasks from Notion with their properties."""
        try:
            logger.info("Querying Notion tasks database...")
            response = await self.client.databases.query(
                **{
                    "database_id": self.tasks_database_id,
                    "filter": {
                        "and": [
                            {
                                "property": "Status",
                                "status": {
                                    "does_not_equal": "Archive"
                                }
                            },
                            {
                                "property": "Status",
                                "status": {
                                    "does_not_equal": "Completed"
                                }
                            }
                        ]
                    }
                }
            )
            
            if not response or "results" not in response:
                logger.error("No results found in Notion response")
                return []

            tasks = []
            for page in response["results"]:
                try:
                    properties = page.get("properties", {})
                    if not properties:
                        logger.warning(f"No properties found for page {page.get('id')}")
                        continue

                    status = get_status_value(properties.get("Status"))
                    # Skip completed or archived tasks
                    if status in ["Completed", "Archive"]:
                        continue

                    task_data = {
                        "id": page.get("id", ""),
                        "title": get_text_content(properties.get("Name")),
                        "importance": get_select_value(properties.get("Importance")),
                        "urgency": get_select_value(properties.get("Urgency")),
                        "status": status
                    }
                    
                    # Only add task if it has required fields
                    if task_data["id"] and task_data["title"]:
                        tasks.append(task_data)
                    else:
                        logger.warning(f"Skipping task due to missing required fields: {task_data}")
                
                except Exception as task_error:
                    logger.error(f"Error processing task: {str(task_error)}")
                    continue
            
            logger.info(f"Successfully fetched {len(tasks)} tasks")
            return tasks
            
        except Exception as e:
            logger.error(f"Error fetching tasks: {str(e)}", exc_info=True)
            return []