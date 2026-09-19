from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "AutoScale Hub v2 - CI/CD is working !!"

@app.route("/health")
def health():
    return "Healthy"

@app.route("/stress")
def stress():
    # Deterministic CPU-bound computation to trigger Kubernetes HPA autoscaling
    result = 0
    for i in range(1_500_000):
        result += (i * i) % 97
    return {"status": "completed", "result": result}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

