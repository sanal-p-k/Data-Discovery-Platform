from typing import Dict, Any

class QueryBuilder:
    def __init__(self, table: str):
        self.table = table
        self.filters = []
        self.limit = None

    def add_filter(self, column: str, operator: str, value: Any):
        """
        Add a filter to the query.
        """
        self.filters.append((column, operator, value))
        return self

    def set_limit(self, limit: int):
        """
        Set a limit for the query.
        """
        self.limit = limit
        return self

    def build(self) -> str:
        """
        Build the SQL query.
        """
        query = f"SELECT * FROM {self.table}"
        if self.filters:
            filters = " AND ".join([f"{col} {op} %s" for col, op, _ in self.filters])
            query += f" WHERE {filters}"
        if self.limit:
            query += f" LIMIT {self.limit}"
        return query

    def get_params(self) -> list:
        """
        Get the parameters for the query.
        """
        return [val for _, _, val in self.filters]