from extract import run_extract
from transform import transform_data
from load import load_big_table

from flask import Flask
import os
import threading

app = Flask(__name__)

# 🟢 This will store logs
logs = []


def log(msg):
    print(msg)  # still show in Render logs
    logs.append(msg)  # store for webpage


@app.route("/")
def home():
    return """
    <h2>ETL Pipeline Status</h2>
    <a href='/logs'>View ETL Logs</a>
    """


@app.route("/logs")
def show_logs():
    return "<br>".join(logs) if logs else "No logs yet..."


def run_etl():

    log(">>> Starting ETL Pipeline <<<")

    log("Step 1: Extracting data…")
    run_extract()
    log("Step 1 Complete.")

    log("Step 2: Transforming data…")
    transform_data()
    log("Step 2 Complete.")

    log("Step 3: Loading data…")
    load_big_table()
    log("Step 3 Complete.")

    log(">>> ETL Pipeline Finished Successfully! <<<")


if __name__ == "__main__":

    # Run ETL in background so web page still loads
    threading.Thread(target=run_etl).start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
