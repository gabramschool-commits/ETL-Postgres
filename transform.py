import pandas as pd
from config import engine

# Currency conversion
JPY_TO_USD = 0.0064
USD_TO_USD = 1


def clean_columns(df):
    """Remove quotes and whitespace from column names."""
    df.columns = df.columns.str.replace("'", "").str.strip()
    return df


def clean_data(df):
    """Drop fully empty rows and fill missing values."""
    df = df.dropna(how="all")

    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)

    cat_cols = df.select_dtypes(include=['object']).columns
    df[cat_cols] = df[cat_cols].fillna("Unknown")

    return df


def convert_currency(df, price_col, rate):
    """Convert price column to standard currency."""
    if price_col in df.columns:
        df[price_col] = (
            pd.to_numeric(df[price_col], errors='coerce')
            .fillna(0) * rate
        )
    return df


def map_japan(conn):

    sales = clean_columns(
        pd.read_sql("SELECT * FROM japan_store_sales_data", conn)
    )

    customers = clean_columns(
        pd.read_sql(
            "SELECT DISTINCT * FROM japan_store_japan_customers",
            conn
        )
    )

    items = clean_columns(
        pd.read_sql(
            "SELECT DISTINCT * FROM japan_store_japan_items",
            conn
        )
    )

    branches = clean_columns(
        pd.read_sql(
            "SELECT DISTINCT * FROM japan_store_japan_branch",
            conn
        )
    )

    payments = clean_columns(
        pd.read_sql(
            "SELECT DISTINCT * FROM japan_store_japan_payment",
            conn
        )
    )

    df = (
        sales
        .merge(customers, left_on="customer_id", right_on="id", how="left")
        .merge(
            items,
            left_on="product_id",
            right_on="id",
            how="left",
            suffixes=("", "_item")
        )
        .merge(
            branches,
            left_on="branch_id",
            right_on="id",
            how="left",
            suffixes=("", "_branch")
        )
        .merge(
            payments,
            left_on="payment",
            right_on="id",
            how="left",
            suffixes=("", "_payment")
        )
    )

    df = clean_data(df)

    # Add store column
    df["store"] = "Japan"

    # Currency conversion
    df["price"] = pd.to_numeric(
        df["price"],
        errors="coerce"
    )

    df = df[df["price"] < 100000]

    df["price"] = (
        df["price"] * JPY_TO_USD
    ).round(2)

    # Rename columns
    df = df.rename(columns={
        "membership": "customer_type",
        "product_name": "product_name",
        "category": "category",
        "name_branch": "branch_name",
        "name_payment": "payment_method"
    })

    # Standardize strings
    str_cols = [
        "customer_type",
        "product_name",
        "category",
        "branch_name",
        "payment_method",
        "gender"
    ]

    for col in str_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.title()
        )

    # Numeric cleanup
    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    ).fillna(0)

    df["rating"] = pd.to_numeric(
        df["rating"],
        errors="coerce"
    ).fillna(0)

    # Remove invalid rows
    df = df[
        (df["quantity"] > 0) &
        (df["price"] > 0)
    ]

    return df[[
        "invoice_id",
        "date",
        "time",
        "store",
        "customer_id",
        "customer_type",
        "gender",
        "product_id",
        "product_name",
        "category",
        "price",
        "quantity",
        "branch_name",
        "payment_method",
        "rating"
    ]]


def map_myanmar(conn):

    sales = clean_columns(
        pd.read_sql(
            "SELECT * FROM myanmar_store_sales_data",
            conn
        )
    )

    customers = clean_columns(
        pd.read_sql(
            "SELECT * FROM myanmar_store_myanmar_customers",
            conn
        )
    )

    items = clean_columns(
        pd.read_sql(
            "SELECT * FROM myanmar_store_myanmar_items",
            conn
        )
    )

    branches = clean_columns(
        pd.read_sql(
            "SELECT * FROM myanmar_store_myanmar_branch",
            conn
        )
    )

    payments = clean_columns(
        pd.read_sql(
            "SELECT * FROM myanmar_store_myanmar_payment",
            conn
        )
    )

    df = (
        sales
        .merge(customers, left_on="customer_id", right_on="id", how="left")
        .merge(
            items,
            left_on="product_id",
            right_on="id",
            how="left",
            suffixes=("", "_item")
        )
        .merge(
            branches,
            left_on="branch_id",
            right_on="id",
            how="left",
            suffixes=("", "_branch")
        )
        .merge(
            payments,
            left_on="payment",
            right_on="id",
            how="left",
            suffixes=("", "_payment")
        )
    )

    # Rename columns
    df = df.rename(columns={
        "name_item": "product_name",
        "type_item": "category",
        "type": "customer_type",
        "name_branch": "branch_name",
        "name_payment": "payment_method"
    })

    # Remove customer name pollution
    if "name" in df.columns:
        df = df.drop(columns=["name"])

    df = clean_data(df)

    # Add store column
    df["store"] = "Myanmar"

    # Numeric cleanup
    df["price"] = pd.to_numeric(
        df["price"],
        errors="coerce"
    ).round(2)

    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    ).fillna(0)

    df["rating"] = pd.to_numeric(
        df["rating"],
        errors="coerce"
    ).fillna(0)

    # Standardize strings
    for col in [
        "customer_type",
        "product_name",
        "category",
        "branch_name",
        "payment_method",
        "gender"
    ]:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.title()
        )

    # Remove invalid rows
    df = df[
        (df["quantity"] > 0) &
        (df["price"] > 0)
    ]

    return df[[
        "invoice_id",
        "date",
        "time",
        "store",
        "customer_id",
        "customer_type",
        "gender",
        "product_id",
        "product_name",
        "category",
        "price",
        "quantity",
        "branch_name",
        "payment_method",
        "rating"
    ]]


def transform_data():

    with engine.begin() as conn:

        japan_df = map_japan(conn)
        myanmar_df = map_myanmar(conn)

        big_table = pd.concat(
            [japan_df, myanmar_df],
            ignore_index=True
        )

        # Deduplicate
        big_table = big_table.drop_duplicates(
            subset=[
                "store",
                "invoice_id",
                "customer_id",
                "product_id"
            ]
        )

        # Remove null critical fields
        big_table = big_table.dropna(
            subset=[
                "invoice_id",
                "customer_id",
                "product_id",
                "branch_name"
            ]
        ).reset_index(drop=True)

        print(
            f"[TRANSFORM] Rows after cleaning: {len(big_table)}"
        )

        # Save to PostgreSQL
        big_table.to_sql(
            "all_sales_big_table",
            conn,
            if_exists="replace",
            index=False
        )

        print(
            "[TRANSFORM] all_sales_big_table created"
        )