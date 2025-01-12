from fastapi import APIRouter, WebSocket, Query
from datetime import datetime, date
from typing import Optional
from ..database.handlers import DatabaseHandler
from pathlib import Path
import yaml
import asyncio
router = APIRouter()

# Load configuration
def load_config():
    try:
        config_path = Path(__file__).parent.parent.parent / 'config' / 'config.yml'
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            return config.get('db_config', {})
    except Exception as e:
        print(f"Error loading config: {e}")
        return {
            'host': 'localhost',
            'port': 3306,
            'database': 'bytelocker',
            'user': 'root',
            'password': ''
        }

# Initialize database handler with config
db_handler = DatabaseHandler(config=load_config())


@router.get("/metrics/crowd")
async def get_crowd_metrics(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = Query(default=100, le=1000)
):
    return db_handler.get_crowd_metrics(start_time, end_time, limit)

@router.get("/metrics/persons")
async def get_person_detections(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    name: Optional[str] = None,
    limit: int = Query(default=100, le=1000)
):
    return db_handler.get_person_detections(start_time, end_time, name, limit)

@router.get("/metrics/safety")
async def get_safety_violations(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    violation_type: Optional[str] = None,
    limit: int = Query(default=100, le=1000)
):
    return db_handler.get_safety_violations(start_time, end_time, violation_type, limit)

@router.get("/metrics/hourly")
async def get_hourly_stats(date: Optional[date] = None):
    return db_handler.get_hourly_stats(date)

@router.websocket("/ws/metrics")
async def websocket_metrics(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Send real-time metrics every second
            metrics = {
                'crowd': db_handler.get_crowd_metrics(limit=1),
                'violations': db_handler.get_safety_violations(limit=1),
                'behavior': db_handler.get_behavior_analytics(limit=1)
            }
            await websocket.send_json(metrics)
            await asyncio.sleep(1)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close() 