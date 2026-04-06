from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./complaints.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Complaint(Base):
    __tablename__ = "complaints"
    
    id = Column(Integer, primary_key=True, index=True)
    complaint_text = Column(Text, nullable=False)
    image_path = Column(String, nullable=False)
    ai_response = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="resolved")

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_complaint(complaint_text: str, image_path: str, ai_response: str):
    db = SessionLocal()
    try:
        complaint = Complaint(
            complaint_text=complaint_text,
            image_path=image_path,
            ai_response=ai_response,
            status="resolved"
        )
        db.add(complaint)
        db.commit()
        db.refresh(complaint)
        return complaint
    finally:
        db.close()

def get_all_complaints():
    db = SessionLocal()
    try:
        return db.query(Complaint).all()
    finally:
        db.close()