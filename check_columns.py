import pandas as pd
from sqlalchemy import create_engine

connection_string = "postgresql+psycopg2://postgres:123456@localhost:5432/postgres"

def check_table_columns():
    try:
        engine = create_engine(connection_string)
        query = "SELECT * FROM fact_taxi_sales LIMIT 1;"
        df = pd.read_sql(query, con=engine)
        print("Actual columns in the 'fact_taxi_sales' table are:")
        print(df.columns.tolist())
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    check_table_columns()
