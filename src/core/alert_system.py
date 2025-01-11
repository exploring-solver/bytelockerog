from datetime import datetime
import queue
from typing import Dict, List
from config.config import SystemConfig
from fastapi import WebSocket
from ..utils.logging_setup import logger
import json
import asyncio

class AlertSystem:
    """Handles alert generation and notification"""
    def __init__(self, config: SystemConfig):
        self.config = config
        self.alert_queue = queue.Queue()
        self.recent_alerts = []  # Store recent alerts for UI
        self.max_recent_alerts = 10  # Maximum number of recent alerts to keep
        print("AlertSystem initialized with config:", self.config)

    def generate_alert(self, alert_type: str, details: Dict):
        """Generate and queue an alert"""
        try:
            print(f"Generating alert of type: {alert_type} with details: {details}")
            # Ensure details are JSON serializable
            serializable_details = {}
            for key, value in details.items():
                if isinstance(value, (int, float, str, bool, list, dict)):
                    serializable_details[key] = value
                else:
                    serializable_details[key] = str(value)
            print(f"Serialized details: {serializable_details}")
            
            alert = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'type': alert_type,
                'details': serializable_details
            }
            
            self.alert_queue.put(alert)
            self.recent_alerts.append(alert)
            print(f"Alert added to queue and recent alerts: {alert}")
            
            # Keep only the most recent alerts
            if len(self.recent_alerts) > self.max_recent_alerts:
                self.recent_alerts = self.recent_alerts[-self.max_recent_alerts:]
                print(f"Trimmed recent alerts list to the latest {self.max_recent_alerts} alerts.")
                
            logger.info(f"Alert generated: {alert_type}")
            
        except Exception as e:
            logger.error(f"Error generating alert: {str(e)}")
            print(f"Error generating alert: {str(e)}")

    def get_alerts(self) -> List[Dict]:
        """Get recent alerts for UI display"""
        print("Returning recent alerts:", self.recent_alerts)
        return self.recent_alerts.copy()  # Return a copy to prevent modification

    async def send_alert(self, websocket: WebSocket):
        """Send alert to connected client"""
        while True:
            if not self.alert_queue.empty():
                try:
                    alert = self.alert_queue.get()
                    print(f"Sending alert: {alert}")
                    # Ensure alert is JSON serializable
                    json_alert = json.dumps(alert, default=str)
                    await websocket.send_text(json_alert)
                    print(f"Alert sent to client: {json_alert}")
                except Exception as e:
                    logger.error(f"Error sending alert: {str(e)}")
                    print(f"Error sending alert: {str(e)}")
            await asyncio.sleep(0.1)
