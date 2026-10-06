import sqlite3

DB_PATH = "monitoring/monitoring.db"


def create_tables():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS deployments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deployment_id TEXT NOT NULL,
            version TEXT NOT NULL,
            status TEXT NOT NULL,
            deployed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usage_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deployment_id TEXT,
            cpu_usage REAL,
            memory_usage REAL,
            request_count INTEGER,
            uptime REAL,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cost_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deployment_id TEXT,
            cpu_cost REAL,
            memory_cost REAL,
            total_cost REAL,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()

    print("Database tables created successfully!")


if __name__ == "__main__":
    create_tables()