from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class SystemConfig:
    """System configuration parameters"""
    min_confidence: float = 0.6
    frame_skip: int = 3
    max_crowd_density: float = 0.75
    restricted_areas: List[List[Tuple[int, int]]] = None
    working_hours: Tuple[int, int] = (9, 17)
    enable_pose_detection: bool = False