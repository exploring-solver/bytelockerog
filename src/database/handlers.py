from datetime import datetime
from typing import Dict
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from ..utils.logging_setup import logger
class DatabaseHandler:
    """Handles database operations with MySQL"""
    def __init__(self, config: dict):
        # Create MySQL connection string
        connection_string = (
            f"mysql+pymysql://{config.get('root', 'root')}:"
            f"{config.get('password', '')}@"
            f"{config.get('host', 'localhost')}/"
            f"{config.get('database', 'bytelocker')}"
        )
        
        try:
            self.engine = create_engine(connection_string)
            Base = declarative_base()
            
            class Event(Base):
                __tablename__ = 'events'
                id = Column(Integer, primary_key=True, autoincrement=True)
                timestamp = Column(DateTime, nullable=False)
                event_type = Column(String(255), nullable=False)
                details = Column(String(1000))
                confidence = Column(Float)
                
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
            self.Event = Event
            
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise

    def log_event(self, event_type: str, details: Dict, confidence: float):
        """Log event to database"""
        session = self.Session()
        try:
            event = self.Event(
                timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                event_type=event_type,
                details=str(details),
                confidence=confidence
            )
            session.add(event)
            session.commit()
        except Exception as e:
            logger.error(f"Database error: {e}")
            session.rollback()
        finally:
            session.close()

