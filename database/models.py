from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class MLEvent(Base):
    __tablename__ = "ml_events"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    model_name = Column(String)
    prediction = Column(Float)
    probability = Column(Float)
    actual_label = Column(Float, nullable=True)
    latency_ms = Column(Integer)
    features = Column(JSON)

class LLMEvent(Base):
    __tablename__ = "llm_events"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    application_name = Column(String)
    prompt = Column(String)
    response = Column(String)
    latency_ms = Column(Integer)
    tokens_used = Column(Integer)
    cost_usd = Column(Float)

class UnifiedMetric(Base):
    __tablename__ = "unified_metrics"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    entity_name = Column(String)
    entity_type = Column(String)  # 'ML' or 'LLM'
    metric_name = Column(String)
    value = Column(Float)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    severity = Column(String)
    message = Column(String)
    resolved = Column(Boolean, default=False)
