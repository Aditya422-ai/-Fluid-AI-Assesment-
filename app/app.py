from flask import Flask
import os
import psycopg2

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")


def check_database():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        conn.close()
        return True
    except Exception:
        return False


@app.route("/")
def home():
    db_status = "OK" if check_database() else "FAILED"

    return f"""
    <h1>DevOps Infrastructure Challenge</h1>
    <p>Backend: Running</p>
    <p>Database: {db_status}</p>
    """


@app.route("/health")
def health():
    if check_database():
        return "healthy", 200
    return "database unavailable", 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
