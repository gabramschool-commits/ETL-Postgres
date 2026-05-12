from config import engine

with engine.connect() as conn:
    print("SUCCESS!")