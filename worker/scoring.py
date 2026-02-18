import re

HALLUCINATION_PHRASES = [
    "as an ai model",
    "i cannot verify",
    "it is possible that",
    "i'm not sure",
    "may not be accurate"
]

def calculate_ml_risk(prediction, drift_api, accuracy=None):
    risk = 0.0
    if drift_api > 0.2:
        risk += 50
    elif drift_api > 0.1:
        risk += 20
        
    if accuracy and accuracy < 0.7:
        risk += 30
        
    return min(risk, 100.0)

def detect_hallucination(response_text):
    text_lower = response_text.lower()
    for phrase in HALLUCINATION_PHRASES:
        if phrase in text_lower:
            return True
    return False

def calculate_llm_risk(latency_ms, cost, hallucination_detected):
    risk = 0.0
    if latency_ms > 2000:
        risk += 20
    if cost > 0.1: # High cost single request
        risk += 30
    if hallucination_detected:
        risk += 50
        
    return min(risk, 100.0)

def calculate_unified_risk(ml_risk, llm_risk):
    return (0.5 * ml_risk) + (0.5 * llm_risk)
