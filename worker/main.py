import os
import json
import redis
import logging
import time
from database.models import MLEvent, LLMEvent, UnifiedMetric, Alert
from worker.db_writer import db_writer
from worker.drift import calculate_psi
from worker.scoring import calculate_ml_risk, calculate_llm_risk, detect_hallucination, calculate_unified_risk

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Basic in-memory aggregator for drift (in production use TimeScale/Redis TimeSeries)
ml_prediction_window = []

def process_ml_event(data, session):
    try:
        event = MLEvent(
            model_name=data.get('model_name'),
            prediction=data.get('prediction'),
            probability=data.get('probability'),
            actual_label=data.get('actual_label'),
            latency_ms=data.get('latency_ms'),
            features=data.get('features')
        )
        session.add(event)
        
        # Add to window for drift calc
        ml_prediction_window.append(data.get('probability', 0))
        if len(ml_prediction_window) > 1000:
            ml_prediction_window.pop(0)
            
        # Calculate Drift
        drift_score = calculate_psi([], ml_prediction_window[-100:]) # Comparing last 100 to mock reference in drift.py
        
        # Calculate Risk
        risk_score = calculate_ml_risk(data.get('prediction'), drift_score)
        
        # Store Metrics
        metrics = [
            UnifiedMetric(entity_name=data.get('model_name'), entity_type='ML', metric_name='drift_psi', value=drift_score),
            UnifiedMetric(entity_name=data.get('model_name'), entity_type='ML', metric_name='risk_score', value=risk_score)
        ]
        session.add_all(metrics)
        
        # Alerting
        if drift_score > 0.2:
            alert = Alert(severity="HIGH", message=f"Drift detected for {data.get('model_name')}: PSI {drift_score:.2f}")
            session.add(alert)
            logger.warning(f"ALERT: Drift detected for {data.get('model_name')}")

        session.commit()
    except Exception as e:
        logger.error(f"Error processing ML event: {e}")
        session.rollback()

def process_llm_event(data, session):
    try:
        event = LLMEvent(
            application_name=data.get('application_name'),
            prompt=data.get('prompt'),
            response=data.get('response'),
            latency_ms=data.get('latency_ms'),
            tokens_used=data.get('tokens_used'),
            cost_usd=data.get('cost_usd')
        )
        session.add(event)
        
        # Logic
        hallucination = detect_hallucination(data.get('response', ''))
        risk_score = calculate_llm_risk(data.get('latency_ms'), data.get('cost_usd'), hallucination)
        
        # Store Metrics
        metrics = [
            UnifiedMetric(entity_name=data.get('application_name'), entity_type='LLM', metric_name='hallucination_flag', value=1.0 if hallucination else 0.0),
            UnifiedMetric(entity_name=data.get('application_name'), entity_type='LLM', metric_name='risk_score', value=risk_score),
            UnifiedMetric(entity_name=data.get('application_name'), entity_type='LLM', metric_name='latency_ms', value=data.get('latency_ms')),
            UnifiedMetric(entity_name=data.get('application_name'), entity_type='LLM', metric_name='cost_usd', value=data.get('cost_usd'))
        ]
        session.add_all(metrics)

        # Alerting
        if hallucination:
             alert = Alert(severity="MEDIUM", message=f"Potential Hallucination for {data.get('application_name')}")
             session.add(alert)
             logger.warning(f"ALERT: Hallucination detected for {data.get('application_name')}")
        
        if risk_score > 80:
             alert = Alert(severity="HIGH", message=f"High Risk Score for {data.get('application_name')}: {risk_score}")
             session.add(alert)

        session.commit()
    except Exception as e:
        logger.error(f"Error processing LLM event: {e}")
        session.rollback()

def main():
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", 6379))
    
    # Wait for DB
    time.sleep(5) 
    db_writer.create_tables()
    
    r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    pubsub = r.pubsub()
    pubsub.subscribe('ml_logs', 'llm_logs')
    
    logger.info("Worker started, listening for events...")
    
    for message in pubsub.listen():
        if message['type'] == 'message':
            channel = message['channel']
            data = json.loads(message['data'])
            
            session = db_writer.get_session()
            try:
                if channel == 'ml_logs':
                    process_ml_event(data, session)
                elif channel == 'llm_logs':
                    process_llm_event(data, session)
            finally:
                session.close()

if __name__ == "__main__":
    main()
