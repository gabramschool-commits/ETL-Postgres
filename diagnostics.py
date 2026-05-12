from config import engine
from sqlalchemy import text


def diagnose():
    print("\n POSTGRESQL DATABASE DIAGNOSTICS\n")

    with engine.connect() as conn:

        tables = conn.execute(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema='public'
            ORDER BY table_name;
        """))

        for table in tables:
            table_name = table[0]

            print(f" TABLE: {table_name}")

            columns = conn.execute(text(f"""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = '{table_name}';
            """))

            print("Columns:")
            for col in columns:
                print(f"  - {col[0]}")

            count = conn.execute(
                text(f"SELECT COUNT(*) FROM {table_name};")
            ).scalar()

            print(f"Row count: {count}\n")


if __name__ == "__main__":
    diagnose()