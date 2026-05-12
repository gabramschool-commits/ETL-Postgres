from config import engine
import pandas as pd


def load_big_table():
    df = pd.read_sql(
        "SELECT * FROM all_sales_big_table",
        engine
    )

    df.to_sql(
        "analytics_sales",
        engine,
        if_exists="replace",
        index=False
    )

    print("[LOAD] analytics_sales loaded")