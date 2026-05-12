import pandas as pd
from config import engine


def run_extract():
    """Load CSV source files into PostgreSQL staging tables."""

    # Japan
    japan_files = {
        "japan_store_sales_data": "data/source/japan_store/sales_data.csv",
        "japan_store_japan_customers": "data/source/japan_store/japan_Customers.csv",
        "japan_store_japan_items": "data/source/japan_store/japan_items.csv",
        "japan_store_japan_branch": "data/source/japan_store/japan_branch.csv",
        "japan_store_japan_payment": "data/source/japan_store/japan_payment.csv",
    }

    for table, file in japan_files.items():
        df = pd.read_csv(file)
        df.to_sql(table, engine, if_exists="replace", index=False)
        print(f"[EXTRACT] {table} loaded")

    # Myanmar
    myanmar_files = {
        "myanmar_store_sales_data": "data/source/myanmar_store/sales_data.csv",
        "myanmar_store_myanmar_customers": "data/source/myanmar_store/myanmar_customers.csv",
        "myanmar_store_myanmar_items": "data/source/myanmar_store/myanmar_items.csv",
        "myanmar_store_myanmar_branch": "data/source/myanmar_store/myanmar_branch.csv",
        "myanmar_store_myanmar_payment": "data/source/myanmar_store/myanmar_payment.csv",
    }

    for table, file in myanmar_files.items():
        df = pd.read_csv(file)
        df.to_sql(table, engine, if_exists="replace", index=False)
        print(f"[EXTRACT] {table} loaded")
