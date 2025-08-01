# Import the QueryBase class
from query_base import QueryBase  # Assuming the previous code is in query_base.py

# Import dependencies needed for sql execution
from sql_execution import execute_sql  # Hypothetical module for SQL execution

import pandas as pd
import sqlite3
from typing import List, Tuple


class Employee(QueryBase):
    """Subclass of QueryBase for querying employee table.

    Provides methods to query employee-specific data from the employee table
    in the employee_events database.
    """
    name: str = "employee"

    def names(self) -> List[Tuple[str, int]]:
        """Retrieve full names and IDs of all employees.

        Returns:
            List[Tuple[str, int]]: List of tuples containing employee full name and ID
        """
        # Query 3
        query = """
            SELECT full_name, employee_id
            FROM employee
        """

        try:
            with sqlite3.connect(self.db_path) as conn:
                # Assuming execute_sql returns a list of tuples
                result = execute_sql(conn, query)
            return result
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    def username(self, id: int) -> List[Tuple[str]]:
        """Retrieve full name for a specific employee ID.

        Args:
            id (int): The employee ID to filter by

        Returns:
            List[Tuple[str]]: List of tuples containing the employee's full name
        """
        # Query 4
        query = f"""
            SELECT full_name
            FROM {self.name}
            WHERE employee_id = {id}
        """

        try:
            with sqlite3.connect(self.db_path) as conn:
                # Assuming execute_sql returns a list of tuples
                result = execute_sql(conn, query)
            return result
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    def model_data(self, id: int) -> pd.DataFrame:
        """Retrieve aggregated event data for machine learning model.

        Args:
            id (int): The employee ID to filter by

        Returns:
            pd.DataFrame: DataFrame containing positive and negative event sums
        """
        query = f"""
            SELECT SUM(positive_events) positive_events
                 , SUM(negative_events) negative_events
            FROM {self.name}
            JOIN employee_events
                USING(employee_id)
            WHERE {self.name}.employee_id = {id}
        """

        try:
            with sqlite3.connect(self.db_path) as conn:
                df = pd.read_sql_query(query, conn)
            return df
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return pd.DataFrame()
