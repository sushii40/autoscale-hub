import time
from collector import collect_metrics


INTERVAL = 60


def start_monitoring():
    print("Automatic monitoring started...")
    print("Collecting metrics every 60 seconds.")

    while True:
        collect_metrics()
        print("Waiting for next collection...")
        time.sleep(INTERVAL)


if __name__ == "__main__":
    start_monitoring()