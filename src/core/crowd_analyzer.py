import numpy as np
from sklearn.cluster import DBSCAN
from typing import List, Dict
from config.config import SystemConfig
from datetime import datetime

class CrowdAnalyzer:
    """Analyzes crowd density and movement patterns"""
    def __init__(self, config: SystemConfig):
        self.config = config
        self.clustering = DBSCAN(eps=30, min_samples=3)
        self.current_analysis = {
            'density': 0.0,
            'hotspots': [],
            'count': 0,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        print(f"CrowdAnalyzer initialized with config: {self.config}")

    def analyze_crowd(self, detections: List[Dict]) -> Dict:
        """Analyze crowd density and patterns"""
        if not detections:
            print("No detections received for analysis.")
            self.current_analysis = {
                'density': 0.0,
                'hotspots': [],
                'count': 0,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            print(f"Analysis result: {self.current_analysis}")
            return self.current_analysis
            
        print(f"Received {len(detections)} detections for analysis.")
        
        points = np.array([[(d['bbox'][0] + d['bbox'][2])/2, 
                           (d['bbox'][1] + d['bbox'][3])/2] for d in detections])
        print(f"Calculated centroid points: {points}")

        clusters = self.clustering.fit_predict(points)
        print(f"DBSCAN clustering results: {clusters}")

        unique_clusters = np.unique(clusters[clusters != -1])
        print(f"Identified unique clusters (excluding noise): {unique_clusters}")

        density = float(len(detections) / (640 * 480))  # normalized by frame size
        print(f"Calculated crowd density: {density}")

        hotspots = []
        for cluster_id in unique_clusters:
            cluster_points = points[clusters == cluster_id]
            center = np.mean(cluster_points, axis=0)
            hotspots.append({
                'center': tuple(map(int, center)),
                'size': len(cluster_points)
            })
            print(f"Identified hotspot: center={center}, size={len(cluster_points)}")
            
        self.current_analysis = {
            'density': density*1000000,
            'hotspots': hotspots,
            'count': len(detections),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        print(f"Analysis result: {self.current_analysis}")

        return self.current_analysis
    
    def get_current_analysis(self) -> Dict:
        """Return the most recent analysis results"""
        print(f"Returning current analysis: {self.current_analysis}")
        return self.current_analysis
