from typing import Dict, List, Optional
from datetime import datetime, timedelta  
from dataclasses import dataclass
import json
from notion_client import Client
import openai
from openai import ChatCompletion
from ..core.config import Settings

class TaskIntelligenceService:
    def __init__(
        self, 
        notion_settings: dict,
        openai_settings: dict
    ):
        self.notion_client = Client(auth=notion_settings["api_key"])
        self.tasks_database_id = notion_settings["tasks_database_id"]
        openai.api_key = openai_settings["api_key"]
        self.model = openai_settings["model"]

    async def analyze_task(self, task_description: str) -> Dict:
        """Analyze a task to estimate duration and other properties."""
        prompt = f"""Analyze this task and provide effort, urgency, and impact ratings (Low/Medium/High):
        Task: {task_description}
        Respond in JSON format with keys: effort, urgency, impact"""
        
        response = await ChatCompletion.acreate(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a task analysis assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        
        analysis = json.loads(response.choices[0].message.content)
        return {
            'effort': {'select': {'name': analysis['effort']}},
            'urgency': {'select': {'name': analysis['urgency']}},
            'impact': {'select': {'name': analysis['impact']}}
        }