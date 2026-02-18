from pydantic import BaseModel, Field
import datetime
from typing import Dict, Optional, Any

class MLLogRequest(BaseModel):
    model_name: str
    prediction: float
    probability: float
    actual_label: Optional[float] = None
    features: Dict[str, Any]
    latency_ms: int

class LLMLogRequest(BaseModel):
    application_name: str
    prompt: str
    response: str
    latency_ms: int
    tokens_used: int
    cost_usd: float

class MetricResponse(BaseModel):
    timestamp: datetime.datetime
    entity_name: str
    metric_name: str
    value: float

class AlertResponse(BaseModel):
    timestamp: datetime.datetime
    severity: str
    message: str
    resolved: bool

class MLLogResponse(MLLogRequest):
    id: str
    timestamp: datetime.datetime

class LLMLogResponse(LLMLogRequest):
    id: str
    timestamp: datetime.datetime

