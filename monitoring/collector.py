import sqlite3
import requests
import psutil

DB_PATH = "monitoring/monitoring.db"
PROMETHEUS_URL = "http://localhost:9090/api/v1/query"

# Demo cloud billing rates
CPU_RATE = 0.01
MEMORY_RATE = 0.005


def get_metric(query):
    try:
        response = requests.get(
            PROMETHEUS_URL,
            params={"query": query},
            timeout=5
        )

        data = response.json()

        if data["data"]["result"]:
            return float(data["data"]["result"][0]["value"][1])

        return 0.0

    except Exception as e:
        print("Error collecting Prometheus metric:", e)
        return 0.0


def collect_metrics():
    # Collect CPU and memory usage
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent

    # Collect application metrics from Prometheus
    request_count = get_metric(
        'sum(flask_http_request_total{job="autoscale-hub"})'
    )

    uptime = get_metric(
        'up{job="autoscale-hub"}'
    )

    # Calculate estimated cost
    cpu_cost = cpu_usage * CPU_RATE
    memory_cost = memory_usage * MEMORY_RATE
    total_cost = cpu_cost + memory_cost

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Store usage data
    cursor.execute("""
        INSERT INTO usage_logs
        (deployment_id, cpu_usage, memory_usage, request_count, uptime)
        VALUES (?, ?, ?, ?, ?)
    """, (
        "deploy-001",
        cpu_usage,
        memory_usage,
        int(request_count),
        uptime
    ))

    # Store cost data
    cursor.execute("""
        INSERT INTO cost_logs
        (deployment_id, cpu_cost, memory_cost, total_cost)
        VALUES (?, ?, ?, ?)
    """, (
        "deploy-001",
        cpu_cost,
        memory_cost,
        total_cost
    ))

    connection.commit()
    connection.close()

    print("Metrics collected successfully!")
    print("CPU usage:", cpu_usage, "%")
    print("Memory usage:", memory_usage, "%")
    print("Request count:", int(request_count))
    print("Uptime:", uptime)
    print("Estimated CPU cost: Rs. ", round(cpu_cost, 4))
    print("Estimated memory cost: Rs. ", round(memory_cost, 4))
    print("Estimated total cost: Rs. ", round(total_cost, 4))


if __name__ == "__main__":
    collect_metrics()
import sqlite3
import requests
import psutil

DB_PATH = "monitoring/monitoring.db"
PROMETHEUS_URL = "http://localhost:9090/api/v1/query"

# Demo cloud billing rates
CPU_RATE = 0.01
MEMORY_RATE = 0.005


def get_metric(query):
    try:
        response = requests.get(
            PROMETHEUS_URL,
            params={"query": query},
            timeout=5
        )

        data = response.json()

        if data["data"]["result"]:
            return float(data["data"]["result"][0]["value"][1])

        return 0.0

    except Exception as e:
        print("Error collecting Prometheus metric:", e)
        return 0.0


def collect_metrics():
    # Collect CPU and memory usage
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent

    # Collect application metrics from Prometheus
    request_count = get_metric(
        'sum(flask_http_request_total{job="autoscale-hub"})'
    )

    uptime = get_metric(
        'up{job="autoscale-hub"}'
    )

    # Calculate estimated cost
    cpu_cost = cpu_usage * CPU_RATE
    memory_cost = memory_usage * MEMORY_RATE
    total_cost = cpu_cost + memory_cost

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Store usage data
    cursor.execute("""
        INSERT INTO usage_logs
        (deployment_id, cpu_usage, memory_usage, request_count, uptime)
        VALUES (?, ?, ?, ?, ?)
    """, (
        "deploy-001",
        cpu_usage,
        memory_usage,
        int(request_count),
        uptime
    ))

    # Store cost data
    cursor.execute("""
        INSERT INTO cost_logs
        (deployment_id, cpu_cost, memory_cost, total_cost)
        VALUES (?, ?, ?, ?)
    """, (
        "deploy-001",
        cpu_cost,
        memory_cost,
        total_cost
    ))

    connection.commit()
    connection.close()

    print("Metrics collected successfully!")
    print("CPU usage:", cpu_usage, "%")
    print("Memory usage:", memory_usage, "%")
    print("Request count:", int(request_count))
    print("Uptime:", uptime)
    print("Estimated CPU cost: ₹", round(cpu_cost, 4))
    print("Estimated memory cost: ₹", round(memory_cost, 4))
    print("Estimated total cost: ₹", round(total_cost, 4))


if __name__ == "__main__":
    collect_metrics()