import pandas as pd
from sqlalchemy import create_engine

# Step 1: Extract data from a CSV file
def extract_data(file_path):
    print("Extracting data...")
    return pd.read_csv(file_path)

# Step 2: Transform data (e.g., clean, filter, or modify)
def transform_data(data):
    print("Transforming data...")
    # Example: Convert column names to lowercase
    data.columns = [col.lower() for col in data.columns]
    return data

# Step 3: Load data into a PostgreSQL database
def load_data(data, db_url, table_name):
    print("Loading data...")
    engine = create_engine(db_url)
    data.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"Data loaded into {table_name} table.")

# Main ETL function
def etl_pipeline():
    # Configuration
    csv_file = "data/sample_data.csv"  # Path to your CSV file
    db_url = "postgresql://user:password@localhost:5432/mydatabase"  # Database URL
    table_name = "sample_table"  # Target table name

    # Run the ETL pipeline
    data = extract_data(csv_file)
    transformed_data = transform_data(data)
    load_data(transformed_data, db_url, table_name)

if __name__ == "__main__":
    etl_pipeline()