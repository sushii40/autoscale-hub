from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Gauge

app = Flask(__name__)

metrics = PrometheusMetrics(app)

# Custom monitoring metrics
cpu_usage = Gauge(
    "autoscale_cpu_usage_percent",
    "Current CPU usage percentage"
)

memory_usage = Gauge(
    "autoscale_memory_usage_percent",
    "Current memory usage percentage"
)

estimated_cost = Gauge(
    "autoscale_estimated_cost",
    "Latest estimated monitoring cost"
)


@app.route("/")
def home():
    return "AutoScale Hub v2 - CI/CD is working !!"


@app.route("/health")
def health():
    return "Healthy"

@app.route("/update-metrics")
def update_metrics():
    import psutil
    import sqlite3

    # Get current CPU and memory usage
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent

    cpu_usage.set(cpu)
    memory_usage.set(memory)

    # Get latest cost from database
    connection = sqlite3.connect("monitoring/monitoring.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT total_cost FROM cost_logs ORDER BY id DESC LIMIT 1"
    )

    result = cursor.fetchone()
    connection.close()

    if result:
        estimated_cost.set(result[0])

    return "Metrics updated successfully"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)