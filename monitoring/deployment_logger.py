import sqlite3
from datetime import datetime

DB_PATH = "monitoring/monitoring.db"


def log_deployment(deployment_id, version, status):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO deployments
        (deployment_id, version, status, deployed_at)
        VALUES (?, ?, ?, ?)
    """, (
        deployment_id,
        version,
        status,
        datetime.now()
    ))

    connection.commit()
    connection.close()

    print("Deployment logged successfully!")
    print("Deployment ID:", deployment_id)
    print("Version:", version)
    print("Status:", status)


if __name__ == "__main__":
    log_deployment(
        "deploy-002",
        "v2.1",
        "SUCCESS"
    )