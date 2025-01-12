from datetime import datetime
from typing import Dict, List
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, JSON, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from ..utils.logging_setup import logger

Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    event_type = Column(String(255), nullable=False)
    details = Column(String(1000))
    confidence = Column(Float)

class CrowdMetrics(Base):
    __tablename__ = 'crowd_metrics'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    density = Column(Float, nullable=False)
    person_count = Column(Integer, nullable=False)
    hotspots = Column(JSON)  # Stores hotspot locations and sizes

class PersonDetections(Base):
    __tablename__ = 'person_detections'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    person_name = Column(String(255))
    confidence = Column(Float)
    location = Column(JSON)  # Stores bbox coordinates

class SafetyViolations(Base):
    __tablename__ = 'safety_violations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    violation_type = Column(String(255))
    location = Column(JSON)
    details = Column(JSON)

class BehaviorAnalytics(Base):
    __tablename__ = 'behavior_analytics'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    anomaly_type = Column(String(255))
    location = Column(JSON)
    details = Column(JSON)

class DatabaseHandler:
    """Handles database operations with MySQL"""
    def __init__(self, config: dict):
        connection_string = (
            f"mysql+pymysql://{config.get('root', 'root')}:"
            f"{config.get('password', '')}@"
            f"{config.get('host', 'localhost')}/"
            f"{config.get('database', 'bytelocker')}"
        )
        
        try:
            self.engine = create_engine(connection_string)
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise

    def log_crowd_metrics(self, density: float, count: int, hotspots: List[Dict]):
        """Log crowd analysis metrics"""
        session = self.Session()
        try:
            metric = CrowdMetrics(
                timestamp=datetime.now(),
                density=density,
                person_count=count,
                hotspots=hotspots
            )
            session.add(metric)
            session.commit()
        except Exception as e:
            logger.error(f"Database error: {e}")
            session.rollback()
        finally:
            session.close()

    def log_person_detection(self, name: str, confidence: float, bbox: tuple):
        """Log person detection"""
        session = self.Session()
        try:
            detection = PersonDetections(
                timestamp=datetime.now(),
                person_name=name,
                confidence=confidence,
                location={'bbox': bbox}
            )
            session.add(detection)
            session.commit()
        except Exception as e:
            logger.error(f"Database error: {e}")
            session.rollback()
        finally:
            session.close()

    def log_safety_violation(self, violation_type: str, location: tuple, details: Dict):
        """Log safety violation"""
        session = self.Session()
        try:
            violation = SafetyViolations(
                timestamp=datetime.now(),
                violation_type=violation_type,
                location={'coordinates': location},
                details=details
            )
            session.add(violation)
            session.commit()
        except Exception as e:
            logger.error(f"Database error: {e}")
            session.rollback()
        finally:
            session.close()

    def log_behavior_anomaly(self, anomaly_type: str, location: tuple, details: Dict):
        """Log behavior anomaly"""
        session = self.Session()
        try:
            anomaly = BehaviorAnalytics(
                timestamp=datetime.now(),
                anomaly_type=anomaly_type,
                location={'coordinates': location},
                details=details
            )
            session.add(anomaly)
            session.commit()
        except Exception as e:
            logger.error(f"Database error: {e}")
            session.rollback()
        finally:
            session.close()

    # Data retrieval methods
    def get_crowd_metrics(self, start_time=None, end_time=None, limit=100):
        """Get crowd metrics within time range"""
        session = self.Session()
        try:
            query = session.query(CrowdMetrics)
            if start_time:
                query = query.filter(CrowdMetrics.timestamp >= start_time)
            if end_time:
                query = query.filter(CrowdMetrics.timestamp <= end_time)
            return query.order_by(CrowdMetrics.timestamp.desc()).limit(limit).all()
        finally:
            session.close()

    def get_person_detections(self, start_time=None, end_time=None, name=None, limit=100):
        """Get person detections with filters"""
        session = self.Session()
        try:
            query = session.query(PersonDetections)
            if start_time:
                query = query.filter(PersonDetections.timestamp >= start_time)
            if end_time:
                query = query.filter(PersonDetections.timestamp <= end_time)
            if name:
                query = query.filter(PersonDetections.person_name == name)
            return query.order_by(PersonDetections.timestamp.desc()).limit(limit).all()
        finally:
            session.close()

    def get_safety_violations(self, start_time=None, end_time=None, violation_type=None, limit=100):
        """Get safety violations with filters"""
        session = self.Session()
        try:
            query = session.query(SafetyViolations)
            if start_time:
                query = query.filter(SafetyViolations.timestamp >= start_time)
            if end_time:
                query = query.filter(SafetyViolations.timestamp <= end_time)
            if violation_type:
                query = query.filter(SafetyViolations.violation_type == violation_type)
            return query.order_by(SafetyViolations.timestamp.desc()).limit(limit).all()
        finally:
            session.close()

    def get_behavior_analytics(self, start_time=None, end_time=None, anomaly_type=None, limit=100):
        """Get behavior analytics with filters"""
        session = self.Session()
        try:
            query = session.query(BehaviorAnalytics)
            if start_time:
                query = query.filter(BehaviorAnalytics.timestamp >= start_time)
            if end_time:
                query = query.filter(BehaviorAnalytics.timestamp <= end_time)
            if anomaly_type:
                query = query.filter(BehaviorAnalytics.anomaly_type == anomaly_type)
            return query.order_by(BehaviorAnalytics.timestamp.desc()).limit(limit).all()
        finally:
            session.close()

    def get_hourly_stats(self, date=None):
        """Get hourly statistics"""
        session = self.Session()
        try:
            query = session.query(
                func.hour(CrowdMetrics.timestamp).label('hour'),
                func.avg(CrowdMetrics.density).label('avg_density'),
                func.avg(CrowdMetrics.person_count).label('avg_count'),
                func.count(CrowdMetrics.id).label('total_records')
            )
            if date:
                query = query.filter(func.date(CrowdMetrics.timestamp) == date)
            return query.group_by(func.hour(CrowdMetrics.timestamp)).all()
        finally:
            session.close()

