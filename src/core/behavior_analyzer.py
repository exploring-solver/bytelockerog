from config.config import SystemConfig
from typing import Dict, List,Tuple
from config.config import SystemConfig

class BehaviorAnalyzer:
    """Analyzes behavior patterns and detects anomalies"""
    def __init__(self, config: SystemConfig):
        self.config = config
        self.movement_history = []
        
    def analyze_behavior(self, detections: List[Dict], 
                        restricted_areas: List[List[Tuple[int, int]]]) -> List[Dict]:
        """Analyze behavior and detect anomalies"""
        anomalies = []
        
        # Check for restricted area violations
        for detection in detections:
            bbox = detection['bbox']
            center = ((bbox[0] + bbox[2])/2, (bbox[1] + bbox[3])/2)
            
            for area in restricted_areas:
                if self._point_in_polygon(center, area):
                    anomalies.append({
                        'type': 'restricted_area_violation',
                        'location': center,
                        'confidence': detection['confidence']
                    })
        
        # Analyze movement patterns
        if len(self.movement_history) > 10:
            current_positions = [(d['bbox'][0] + d['bbox'][2])/2 for d in detections]
            
            # Detect sudden movements
            for i, hist in enumerate(self.movement_history[-2:]):
                if abs(current_positions[i] - hist) > 100:  # threshold for sudden movement
                    anomalies.append({
                        'type': 'sudden_movement',
                        'location': (current_positions[i], detections[i]['bbox'][1]),
                        'confidence': detections[i]['confidence']
                    })
                    
            self.movement_history = self.movement_history[-10:]
        
        self.movement_history.extend([d['bbox'][0] for d in detections])
        return anomalies
    
    def _point_in_polygon(self, point: Tuple[float, float], 
                         polygon: List[Tuple[int, int]]) -> bool:
        """Check if point is inside polygon"""
        x, y = point
        n = len(polygon)
        inside = False
        
        p1x, p1y = polygon[0]
        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside
