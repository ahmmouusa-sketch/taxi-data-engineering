import os
import pandas as pd
from sqlalchemy import create_engine

# 1. مسار ملف البيانات النظيف
csv_file_path = os.path.join("data", "cleaned", "sales_data_clean.csv")

# 2. إعدادات الاتصال المباشرة
DB_USER = "postgres"
DB_PASSWORD = "123456"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "postgres"

# استخدام psycopg2 engine string المحدد
connection_string = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def load_data_to_postgres():
    try:
        print("Reading the cleaned data file...")
        df = pd.read_csv(csv_file_path)
        print(f"Successfully read {len(df)} rows.")

        # إنشاء المحرك
        engine = create_engine(connection_string)

        print("Uploading data into 'fact_taxi_sales' table in PostgreSQL...")
        
        # رفع الداتا للجدول
        df.to_sql('fact_taxi_sales', con=engine, if_exists='replace', index=False)

        print("Data successfully loaded into the database!")

    except Exception as e:
        print(f"Error occurred while loading data: {e}")

if __name__ == "__main__":
    load_data_to_postgres()