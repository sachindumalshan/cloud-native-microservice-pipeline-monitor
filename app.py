from fastapi import FastAPI, Response
from prometheus_client import Counter, Gauge, generate_latest

import random, time

app = FastAPI()

# Prometheus metrics
REQUEST_COUNT = Counter('app_requests_total', 'Total API requests')
CPU_USAGE = Gauge('cpu_usage_percent', 'CPU usage percent')
MEMORY_USAGE = Gauge('memory_usage_percent', 'Memory usage percent')

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/metrics")
def metrics_endpoint():
    # Simulate metrics
    CPU_USAGE.set(random.uniform(0, 100))
    MEMORY_USAGE.set(random.uniform(0, 100))
    REQUEST_COUNT.inc()
    return Response(generate_latest(), media_type="text/plain")

@app.post("/simulate_load")
def simulate_load(duration: int = 5):
    start = time.time()
    while time.time() - start < duration:
        sum([i**2 for i in range(10000)])
    return {"status": "load simulated"}
