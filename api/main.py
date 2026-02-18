import logging
import uuid
import datetime
from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc

from api.models import MLLogRequest, LLMLogRequest, MetricResponse, AlertResponse, MLLogResponse, LLMLogResponse
from api.producer import producer
from api.database import get_db
from database.models import UnifiedMetric, Alert, MLEvent, LLMEvent

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Unified AI Observability Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For MVP, allow all. In production, specify ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "api"}

@app.post("/log-ml")
def log_ml(event: MLLogRequest):
    try:
        payload = event.model_dump()
        payload['id'] = str(uuid.uuid4())
        payload['timestamp'] = datetime.datetime.utcnow().isoformat()
        
        producer.publish("ml_logs", payload)
        logger.info(f"Published ML event: {payload['id']}")
        return {"status": "queued", "id": payload['id']}
    except Exception as e:
        logger.error(f"Error publishing ML event: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/log-llm")
def log_llm(event: LLMLogRequest):
    try:
        payload = event.model_dump()
        payload['id'] = str(uuid.uuid4())
        payload['timestamp'] = datetime.datetime.utcnow().isoformat()
        
        producer.publish("llm_logs", payload)
        logger.info(f"Published LLM event: {payload['id']}")
        return {"status": "queued", "id": payload['id']}
    except Exception as e:
        logger.error(f"Error publishing LLM event: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/metrics", response_model=List[MetricResponse])
def get_metrics(limit: int = 100, db: Session = Depends(get_db)):
    metrics = db.query(UnifiedMetric).order_by(desc(UnifiedMetric.timestamp)).limit(limit).all()
    return metrics

@app.get("/alerts", response_model=List[AlertResponse])
def get_alerts(limit: int = 50, db: Session = Depends(get_db)):
    alerts = db.query(Alert).order_by(desc(Alert.timestamp)).limit(limit).all()
    return alerts

@app.get("/events/ml", response_model=List[MLLogResponse])
def get_ml_events(limit: int = 50, db: Session = Depends(get_db)):
    events = db.query(MLEvent).order_by(desc(MLEvent.timestamp)).limit(limit).all()
    # Convert SQLAlchemy objects to dict/Pydantic
    return events

@app.get("/events/llm", response_model=List[LLMLogResponse])
def get_llm_events(limit: int = 50, db: Session = Depends(get_db)):
    events = db.query(LLMEvent).order_by(desc(LLMEvent.timestamp)).limit(limit).all()
    return events
