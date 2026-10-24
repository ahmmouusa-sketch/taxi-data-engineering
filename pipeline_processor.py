import logging
import sys
from typing import Optional
import polars as pl
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Configure structured logging for the data pipeline
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("PolarsPipelineLogger")


def extract_and_transform_with_polars(file_path: str) -> Optional[pl.DataFrame]:
  """Reads raw sales CSV data using Polars, cleans missing values,

  enforces schema types matching the exact dataset columns, and prepares it for
  loading.
  """
  try:
    logger.info(f"Starting data extraction with Polars from source: {file_path}")

    # Read data using Polars
    df = pl.read_csv(file_path)

    initial_row_count = len(df)

    # Data validation and cleaning: Drop rows with critical null identifiers using exact column names
    df = df.drop_nulls(subset=["order_id", "customer_name"])
    cleaned_row_count = len(df)

    logger.info(
        f"Dropped {initial_row_count - cleaned_row_count} rows due to missing"
        " critical identifiers."
    )

    # Enforce strict type casting in Polars matching your CSV schema
    df = df.with_columns([
        pl.col("quantity").cast(pl.Int64, strict=False),
        pl.col("unit_price").cast(pl.Float64, strict=False),
        pl.col("total_price").cast(pl.Float64, strict=False),
    ])

    logger.info("Polars data transformation and cleaning completed successfully.")
    return df

  except FileNotFoundError:
    logger.error(f"The file {file_path} was not found.")
    return None
  except Exception as e:
    logger.exception(f"Unexpected error during Polars transformation phase: {e}")
    return None


def load_polars_to_postgres(df: pl.DataFrame, connection_string: str) -> bool:
  """Converts the Polars DataFrame to Pandas temporarily and loads it

  into PostgreSQL using SQLAlchemy.
  """
  try:
    logger.info("Initializing database connection engine.")
    engine = create_engine(connection_string)

    # Convert Polars to Pandas DataFrame for seamless SQLAlchemy compatibility
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
  # Configuration parameters with the correct relative path to your CSV file
  SOURCE_CSV = "data/raw/sales_data.csv"
  DB_CONNECTION_URI = (
      "postgresql+psycopg2://postgres:123456@localhost:5432/postgres"
  )

  logger.info("--- Polars Pipeline execution started ---")

  # Execute Pipeline Steps
  transformed_df = extract_and_transform_with_polars(SOURCE_CSV)

  if transformed_df is not None and not transformed_df.is_empty():
    load_success = load_polars_to_postgres(transformed_df, DB_CONNECTION_URI)
    if load_success:
      logger.info(
          "--- Polars Pipeline execution completed successfully ---"
      )
    else:
      logger.error("--- Polars Pipeline failed during the load phase ---")
  else:
    logger.warning(
        "--- Polars Pipeline aborted: No valid data to process or extraction"
        " failed ---"
    )