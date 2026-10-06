"""
AutoScale Hub Load Testing Script (Python Fallback / Alternative to k6)
Generates high concurrent HTTP traffic to the /stress endpoint to trigger HPA scaling.
"""

import sys
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor

TARGET_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000/stress"
CONCURRENCY = 25
DURATION_SECONDS = 60

print(f"==================================================")
print(f"Starting Load Test on {TARGET_URL}")
print(f"Concurrent Workers: {CONCURRENCY}")
print(f"Duration: {DURATION_SECONDS} seconds")
print(f"==================================================")

success_count = 0
failure_count = 0
start_time = time.time()


def send_request():
    global success_count, failure_count
    try:
        req = urllib.request.Request(TARGET_URL, headers={"User-Agent": "AutoScaleHub-LoadTester"})
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                success_count += 1
            else:
                failure_count += 1
    except Exception:
        failure_count += 1


def worker_loop():
    while time.time() - start_time < DURATION_SECONDS:
        send_request()


with ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
    futures = [executor.submit(worker_loop) for _ in range(CONCURRENCY)]
    for f in futures:
        f.result()

total_time = round(time.time() - start_time, 2)
total_requests = success_count + failure_count
rps = round(total_requests / total_time, 2) if total_time > 0 else 0

print(f"\n==================================================")
print(f"Load Test Complete!")
print(f"Total Requests Sent: {total_requests}")
print(f"Successful (200 OK): {success_count}")
print(f"Failed: {failure_count}")
print(f"Total Duration: {total_time}s")
print(f"Throughput: {rps} req/sec")
print(f"Check HPA with: kubectl get hpa autoscale-hub-hpa --watch")
print(f"==================================================")
