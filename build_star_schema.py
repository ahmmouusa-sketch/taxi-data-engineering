import pandas as pd
from sqlalchemy import create_engine, text

# Database connection settings
DB_CONNECTION_STRING = "postgresql+psycopg2://postgres:123456@localhost:5432/postgres"

def create_star_schema():
    try:
        engine = create_engine(DB_CONNECTION_STRING)
        
        # 1. Fetch raw data from the current base table
        print("Reading base data from 'fact_taxi_sales'...")
        raw_df = pd.read_sql("SELECT * FROM fact_taxi_sales;", con=engine)
        
        # 2. Build Dimension Table: dim_customers
        print("Creating 'dim_customers' table...")
        customers_df = raw_df[['customer_name', 'customer_age', 'customer_gender', 'city']].drop_duplicates().reset_index(drop=True)
        customers_df['customer_id'] = customers_df.index + 1
        
        # 3. Build Dimension Table: dim_products
        print("Creating 'dim_products' table...")
        products_df = raw_df[['product', 'category']].drop_duplicates().reset_index(drop=True)
        products_df['product_id'] = products_df.index + 1
        
        # 4. Build Fact Table: fact_sales
        print("Creating 'fact_sales' table...")
        fact_df = raw_df.merge(customers_df, on=['customer_name', 'customer_age', 'customer_gender', 'city'])
        fact_df = fact_df.merge(products_df, on=['product', 'category'])
        
        # Select required columns for the Fact Table
        fact_sales = fact_df[['order_id', 'customer_id', 'product_id', 'quantity', 'unit_price', 'total_price']]
        
        # 5. Write new tables into PostgreSQL Database
        with engine.begin() as conn:
            customers_df[['customer_id', 'customer_name', 'customer_age', 'customer_gender', 'city']].to_sql('dim_customers', con=conn, if_exists='replace', index=False)
            products_df[['product_id', 'product', 'category']].to_sql('dim_products', con=conn, if_exists='replace', index=False)
            fact_sales.to_sql('fact_sales', con=conn, if_exists='replace', index=False)
            
        print("Star Schema created successfully in the database!")

    except Exception as e:
        print(f"An error occurred while building Star Schema: {e}")

if __name__ == "__main__":
    create_star_schema()