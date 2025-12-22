from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse, JSONResponse
from prometheus_client import Counter, Gauge, generate_latest
import random, time, psutil

app = FastAPI()

# =======================
# Prometheus Metrics
# =======================
REQUEST_COUNT = Counter(
    "app_requests_total", "Total API requests"
)
CPU_USAGE = Gauge(
    "cpu_usage_percent", "CPU usage percent"
)
MEMORY_USAGE = Gauge(
    "memory_usage_percent", "Memory usage percent"
)

# =======================
# Root endpoint - Beautiful landing page
# =======================
@app.get("/", response_class=HTMLResponse)
def root():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Health Metrics Service</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 24px;
            padding: 60px 40px;
            max-width: 600px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
        }
        h1 {
            font-size: 2.5rem;
            color: #667eea;
            margin-bottom: 20px;
            font-weight: 700;
        }
        .emoji {
            font-size: 4rem;
            margin-bottom: 20px;
        }
        p {
            color: #4a5568;
            font-size: 1.1rem;
            line-height: 1.6;
            margin-bottom: 40px;
        }
        .links {
            display: grid;
            gap: 15px;
        }
        .link-btn {
            display: block;
            padding: 18px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        .link-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        .link-btn.secondary {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
        }
        .link-btn.secondary:hover {
            box-shadow: 0 6px 20px rgba(245, 87, 108, 0.6);
        }
        .link-btn.tertiary {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            box-shadow: 0 4px 15px rgba(79, 172, 254, 0.4);
        }
        .link-btn.tertiary:hover {
            box-shadow: 0 6px 20px rgba(79, 172, 254, 0.6);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="emoji">🚀</div>
        <h1>Health Metrics Service</h1>
        <p>Welcome to the enterprise monitoring and health check system. Access real-time metrics and dashboards below.</p>
        <div class="links">
            <a href="/dashboard" class="link-btn">📊 Live Dashboard</a>
            <a href="/health-page" class="link-btn secondary">💚 Health Status Page</a>
            <a href="/metrics" class="link-btn tertiary">📈 Prometheus Metrics</a>
        </div>
    </div>
</body>
</html>
"""

# =======================
# Health endpoint - JSON (for tests/monitoring)
# =======================
@app.get("/health")
def health_check_json():
    return {"status": "healthy"}

# =======================
# Health page - Beautiful status page
# =======================
@app.get("/health-page", response_class=HTMLResponse)
def health_check_page():
    cpu = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory().percent
    
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Health Check</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .container {{
            background: white;
            border-radius: 24px;
            padding: 50px 40px;
            max-width: 500px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
        }}
        .status-icon {{
            font-size: 5rem;
            margin-bottom: 20px;
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.1); }}
        }}
        h1 {{
            color: #11998e;
            font-size: 2.5rem;
            margin-bottom: 15px;
            font-weight: 700;
        }}
        .status {{
            display: inline-block;
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 12px 30px;
            border-radius: 25px;
            font-weight: 600;
            font-size: 1.2rem;
            margin-bottom: 30px;
        }}
        .metrics {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 30px;
        }}
        .metric-card {{
            background: #f7fafc;
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid #11998e;
        }}
        .metric-label {{
            color: #718096;
            font-size: 0.9rem;
            margin-bottom: 8px;
        }}
        .metric-value {{
            color: #2d3748;
            font-size: 1.8rem;
            font-weight: 700;
        }}
        .back-btn {{
            display: inline-block;
            margin-top: 30px;
            padding: 12px 30px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        .back-btn:hover {{
            background: #764ba2;
            transform: translateY(-2px);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="status-icon">✅</div>
        <h1>System Healthy</h1>
        <div class="status">All Systems Operational</div>
        
        <div class="metrics">
            <div class="metric-card">
                <div class="metric-label">CPU Usage</div>
                <div class="metric-value">{cpu:.1f}%</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Memory</div>
                <div class="metric-value">{memory:.1f}%</div>
            </div>
        </div>
        
        <a href="/" class="back-btn">← Back to Home</a>
    </div>
</body>
</html>
"""

# =======================
# Prometheus metrics - Beautiful visualization
# =======================
@app.get("/metrics", response_class=HTMLResponse)
def metrics_endpoint():
    CPU_USAGE.set(psutil.cpu_percent(interval=0.1))
    MEMORY_USAGE.set(psutil.virtual_memory().percent)
    REQUEST_COUNT.inc()
    
    prometheus_data = generate_latest().decode('utf-8')
    
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prometheus Metrics</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            font-family: 'Courier New', monospace;
            min-height: 100vh;
            padding: 40px 20px;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        .header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 3px solid #3b82f6;
        }}
        h1 {{
            color: #1e3a8a;
            font-size: 2rem;
            font-weight: 700;
        }}
        .prometheus-logo {{
            font-size: 2.5rem;
        }}
        .metrics-box {{
            background: #f8fafc;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 30px;
            font-family: 'Courier New', monospace;
            font-size: 0.95rem;
            line-height: 1.8;
            color: #334155;
            white-space: pre-wrap;
            word-wrap: break-word;
            max-height: 500px;
            overflow-y: auto;
        }}
        .metrics-box::-webkit-scrollbar {{
            width: 8px;
        }}
        .metrics-box::-webkit-scrollbar-track {{
            background: #e2e8f0;
            border-radius: 4px;
        }}
        .metrics-box::-webkit-scrollbar-thumb {{
            background: #3b82f6;
            border-radius: 4px;
        }}
        .info-banner {{
            background: linear-gradient(135deg, #3b82f6 0%, #1e3a8a 100%);
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 0.95rem;
        }}
        .back-btn {{
            display: inline-block;
            margin-top: 20px;
            padding: 12px 30px;
            background: #3b82f6;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            font-family: 'Segoe UI', sans-serif;
            transition: all 0.3s ease;
        }}
        .back-btn:hover {{
            background: #1e3a8a;
            transform: translateY(-2px);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📈 Prometheus Metrics</h1>
            <div class="prometheus-logo">🔥</div>
        </div>
        
        <div class="info-banner">
            ℹ️ These metrics are in Prometheus exposition format, ready to be scraped by Prometheus server
        </div>
        
        <div class="metrics-box">{prometheus_data}</div>
        
        <a href="/" class="back-btn">← Back to Home</a>
    </div>
</body>
</html>
"""

# =======================
# JSON stats for frontend
# =======================
@app.get("/api/stats")
def stats():
    return JSONResponse({
        "cpu": psutil.cpu_percent(interval=0.1),
        "memory": psutil.virtual_memory().percent,
        "requests": REQUEST_COUNT._value.get()
    })

# =======================
# Enhanced dashboard with real-time charts
# =======================
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Health Metrics Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #e2e8f0;
            padding: 20px;
            min-height: 100vh;
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        h1 {
            font-size: 2.5rem;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            font-weight: 700;
        }
        .subtitle {
            color: #94a3b8;
            font-size: 1.1rem;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .card {
            background: rgba(30, 41, 59, 0.8);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(59, 130, 246, 0.3);
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 48px rgba(59, 130, 246, 0.4);
            border-color: rgba(59, 130, 246, 0.6);
        }
        .card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
        }
        .card-title {
            font-size: 0.95rem;
            color: #94a3b8;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .card-icon {
            font-size: 1.8rem;
        }
        .value {
            font-size: 3.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 15px 0;
        }
        .progress-bar {
            width: 100%;
            height: 8px;
            background: rgba(59, 130, 246, 0.2);
            border-radius: 4px;
            overflow: hidden;
            margin-top: 15px;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
            border-radius: 4px;
            transition: width 0.5s ease;
        }
        .status-badge {
            display: inline-block;
            padding: 6px 16px;
            background: rgba(34, 197, 94, 0.2);
            border: 1px solid rgba(34, 197, 94, 0.4);
            color: #22c55e;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-top: 10px;
        }
        .back-btn {
            display: block;
            max-width: 200px;
            margin: 40px auto 0;
            padding: 14px 30px;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            color: white;
            text-decoration: none;
            border-radius: 10px;
            font-weight: 600;
            text-align: center;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
        }
        .back-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.6);
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .card {
            animation: fadeIn 0.5s ease;
        }
        .card:nth-child(2) { animation-delay: 0.1s; }
        .card:nth-child(3) { animation-delay: 0.2s; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Health Metrics Dashboard</h1>
        <p class="subtitle">Real-time system monitoring and performance metrics</p>
    </div>

    <div class="grid">
        <div class="card">
            <div class="card-header">
                <div class="card-title">CPU Usage</div>
                <div class="card-icon">🖥️</div>
            </div>
            <div class="value"><span id="cpu">--</span>%</div>
            <div class="progress-bar">
                <div class="progress-fill" id="cpu-bar" style="width: 0%"></div>
            </div>
            <div class="status-badge">● Active</div>
        </div>

        <div class="card">
            <div class="card-header">
                <div class="card-title">Memory Usage</div>
                <div class="card-icon">💾</div>
            </div>
            <div class="value"><span id="memory">--</span>%</div>
            <div class="progress-bar">
                <div class="progress-fill" id="memory-bar" style="width: 0%"></div>
            </div>
            <div class="status-badge">● Active</div>
        </div>

        <div class="card">
            <div class="card-header">
                <div class="card-title">Total Requests</div>
                <div class="card-icon">📈</div>
            </div>
            <div class="value"><span id="requests">--</span></div>
            <div class="status-badge">● Counting</div>
        </div>
    </div>

    <a href="/" class="back-btn">← Back to Home</a>

    <script>
        async function refresh() {
            try {
                const res = await fetch("/api/stats");
                const data = await res.json();
                
                document.getElementById("cpu").innerText = data.cpu.toFixed(1);
                document.getElementById("memory").innerText = data.memory.toFixed(1);
                document.getElementById("requests").innerText = data.requests;
                
                document.getElementById("cpu-bar").style.width = data.cpu + "%";
                document.getElementById("memory-bar").style.width = data.memory + "%";
            } catch (err) {
                console.error("Failed to fetch stats:", err);
            }
        }

        setInterval(refresh, 2000);
        refresh();
    </script>
</body>
</html>
"""