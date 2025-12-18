from fastapi import FastAPI
import random, time

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/metrics")
def metrics():
    cpu_load = random.uniform(0, 100)
    memory_usage = random.uniform(0, 100)
    return {"cpu": cpu_load, "memory": memory_usage}

@app.post("/simulate_load")
def simulate_load(duration: int = 5):
    start = time.time()
    while time.time() - start < duration:
        sum([i**2 for i in range(10000)])
    return {"status": "load simulated"}
