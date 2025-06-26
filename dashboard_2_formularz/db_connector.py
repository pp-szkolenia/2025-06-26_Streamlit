import pandas as pd
from sqlalchemy import create_engine


class DatabaseConnector:
    def __init__(self, db_path: str = "data.db"):
        self.db_path = db_path
        self.engine = create_engine(f"sqlite:///{db_path}")

    def add_record(self, table_name: str, record: dict):
        if not isinstance(record, dict):
            raise ValueError("`record` must be a dict")

        df_existing = pd.read_sql(f"SELECT * FROM {table_name}", self.engine)
        existing_cols = list(df_existing.columns)

        record_keys = set(record.keys())
        expected_keys = set(existing_cols)
        if not record_keys <= expected_keys:
            extra = record_keys - expected_keys
            raise ValueError(f"Unexpected columns in record: {extra}")

        df = pd.DataFrame([record], columns=existing_cols)
        df.to_sql(table_name, self.engine, if_exists="append", index=False)

    def select_records(self, table_name: str) -> pd.DataFrame:
        return pd.read_sql(f"SELECT * FROM {table_name}", self.engine)

    def update_table(self, table_name: str, df: pd.DataFrame):
        if not isinstance(df, pd.DataFrame):
            raise ValueError("`df` must be a pandas DataFrame")

        df.to_sql(table_name, self.engine, if_exists="replace", index=False)
