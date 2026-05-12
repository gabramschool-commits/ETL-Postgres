from extract import run_extract
from transform import transform_data
from load import load_big_table

from flask import Flask
import threading
import os

app = Flask(__name__)


@app.route("/")
def home():
    return "ETL Pipeline Running Successfully"


def run_etl():

    print(">>> Starting ETL Pipeline <<<\n")

    print("Step 1: Extracting data…")
    run_extract()
    print("Step 1 Complete.\n")

    print("Step 2: Transforming data…")
    transform_data()
    print("Step 2 Complete.\n")

    print("Step 3: Loading data…")
    load_big_table()
    print("Step 3 Complete.\n")

    print(">>> ETL Pipeline Finished Successfully! <<<")


if __name__ == "__main__":

    # Run ETL in background
    threading.Thread(target=run_etl).start()

    # Open web port for Render
    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)
