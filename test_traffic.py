import requests
import random
import time
import uuid

API_URL = "http://localhost:8000"

MODELS = ["fraud_model_v1", "recommendation_engine_v2"]
APPS = ["customer_chatbot", "internal_qa_bot"]

def generate_ml_event():
    model = random.choice(MODELS)
    # Simulate drift for fraud_model_v1
    if model == "fraud_model_v1" and random.random() > 0.8:
         prob = random.uniform(0.7, 0.99) # Higher prob -> drift if baseline is low
    else:
         prob = random.uniform(0.1, 0.4)
         
    event = {
        "model_name": model,
        "prediction": 1 if prob > 0.5 else 0,
        "probability": prob,
        "actual_label": 1 if random.random() > 0.9 else 0,
        "features": {
            "amount": random.uniform(10, 1000),
            "merchant_id": str(uuid.uuid4())[:8]
        },
        "latency_ms": random.randint(10, 200)
    }
    
    try:
        resp = requests.post(f"{API_URL}/log-ml", json=event)
        print(f"ML Logged: {resp.status_code} - {event['model_name']}")
    except Exception as e:
        print(f"Error logging ML: {e}")

def generate_llm_event():
    app = random.choice(APPS)
    hallucination = random.choice([True, False, False, False]) # 25% chance
    
    response = "This is a helpful response."
    if hallucination:
        response = "I'm not sure, but as an AI model, I think the answer is 42."
        
    event = {
        "application_name": app,
        "prompt": "What is the meaning of life?",
        "response": response,
        "latency_ms": random.randint(500, 5000),
        "tokens_used": random.randint(50, 1000),
        "cost_usd": random.uniform(0.001, 0.05)
    }
    
    try:
        resp = requests.post(f"{API_URL}/log-llm", json=event)
        print(f"LLM Logged: {resp.status_code} - {event['application_name']}")
    except Exception as e:
        print(f"Error logging LLM: {e}")

if __name__ == "__main__":
    print("Starting traffic generator...")
    while True:
        if random.random() > 0.5:
            generate_ml_event()
        else:
            generate_llm_event()
        time.sleep(1)
