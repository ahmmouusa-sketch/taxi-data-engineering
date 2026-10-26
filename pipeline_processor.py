import logging
import sys
from typing import Optional
import polars as pl
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("PolarsPipelineLogger")


def extract_and_transform_lazy(file_path: str) -> Optional[pl.DataFrame]:
  """Reads raw sales CSV data using Polars Lazy API for high performance,

  applies predicate pushdown, cleans data, and collects the result.
  """
  try:
    logger.info(
        f"Starting lazy data extraction with Polars from source: {file_path}"
    )

    # 1. استخدام scan_csv بدلاً من read_csv للتعامل مع الـ LazyFrame
    q = (
        pl.scan_csv(file_path)
        # 2. تصفية البيانات مبكراً (Predicate Pushdown) لتقليل حجم البيانات المعالجة
        .filter(pl.col("order_id").is_not_null() & pl.col("customer_name").is_not_null())
        # 3. اختيار الأعمدة الأساسية المطلوبة فقط (Projection Pushdown)
        .select([
            "order_id",
            "customer_name",
            "customer_age",
            "customer_gender",
            "city",
            "product",
            "category",
            "quantity",
            "unit_price",
            "total_price",
        ])
    )

    # فرض أنواع البيانات أثناء تجميع الـ Lazy Plan
    # (Polars يقوم بتحسين خطة التنفيذ بالكامل هنا)
    df = q.collect()

    logger.info(
        "Polars lazy transformation and query optimization completed"
        " successfully."
    )
    return df

  except FileNotFoundError:
    logger.error(f"The file {file_path} was not found.")
    return None
  except Exception as e:
    logger.exception(f"Unexpected error during Polars lazy pipeline phase: {e}")
    return None


def load_polars_to_postgres(df: pl.DataFrame, connection_string: str) -> bool:
  try:
    logger.info("Initializing database connection engine.")
    engine = create_engine(connection_string)

    pandas_df = df.to_pandas()

    logger.info(
        "Loading data into PostgreSQL target table: 'fact_sales_processed'"
    )
    with engine.begin() as connection:
      pandas_df.to_sql(
          name="fact_sales_processed",
          con=connection,
          if_exists="append",
          index=False,
      )

    logger.info("Data successfully loaded into PostgreSQL.")
    return True

  except SQLAlchemyError as db_err:
    logger.error(f"Database error occurred during load phase: {db_err}")
    return False
  except Exception as e:
    logger.exception(f"Failed to load data into database: {e}")
    return False


if __name__ == "__main__":
  SOURCE_CSV = "data/raw/sales_data.csv"
  DB_CONNECTION_URI = (
      "postgresql+psycopg2://postgres:123456@localhost:5432/postgres"
  )

  logger.info("--- Optimized Polars Pipeline execution started ---")

  transformed_df = extract_and_transform_lazy(SOURCE_CSV)

  if transformed_df is not None and not transformed_df.is_empty():
    load_success = load_polars_to_postgres(transformed_df, DB_CONNECTION_URI)
    if load_success:
      logger.info(
          "--- Optimized Polars Pipeline execution completed successfully ---"
      )
    else:
      logger.error("--- Pipeline failed during the load phase ---")
  else:
    logger.warning("--- Pipeline aborted: No valid data to process ---")