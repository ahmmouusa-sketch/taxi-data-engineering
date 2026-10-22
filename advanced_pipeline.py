import pandas as pd
from sqlalchemy import create_engine
import time

# 1. Database Connection String (PostgreSQL)
DB_CONNECTION_STRING = "postgresql+psycopg2://postgres:123456@localhost:5432/postgres"

def process_sales_data_in_chunks():
    try:
        engine = create_engine(DB_CONNECTION_STRING)
        
        # Advanced SQL Query with Aggregations
        query = """
            SELECT 
                city,
                category,
                COUNT(order_id) as total_orders,
                SUM(total_price) as total_revenue,
                AVG(customer_age) as avg_customer_age
            FROM fact_taxi_sales
            GROUP BY city, category;
        """
        
        print("Executing query and fetching data efficiently...")
        start_time = time.time()
        
        # Read data using pandas with chunking optimization (best practice for large datasets)
        df_iter = pd.read_sql(query, con=engine, chunksize=1000)
        
        chunk_list = []
        for chunk in df_iter:
            # Here you can apply any transformation logic per chunk
            chunk_list.append(chunk)
            
        final_df = pd.concat(chunk_list, ignore_index=True)
        
        print(f"Data processed successfully in {time.time() - start_time:.2f} seconds!")
        print(final_df.head());

    except Exception as e:
        print(f"An error occurred during pipeline execution: {e}")

if __name__ == "__main__":
    process_sales_data_in_chunks()