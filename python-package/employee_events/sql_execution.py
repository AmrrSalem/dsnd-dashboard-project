from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd

# Using pathlib, create a db_path variable that points to the absolute path
# for the employee_events.db file
db_path = Path(__file__).parent.absolute() / "employee_events.db"

# OPTION 1: MIXIN
class QueryMixin:
    """Mixin class providing methods for executing SQL queries.

    Offers utility methods to execute SQL queries and return results
    as pandas DataFrames or lists of tuples.
    """

    def pandas_query(self, sql_query: str) -> pd.DataFrame:
        """Execute an SQL query and return the result as a pandas DataFrame.

        Args:
            sql_query (str): The SQL query to execute

        Returns:
            pd.DataFrame: DataFrame containing the query results
        """
        try:
            with connect(db_path) as conn:
                df = pd.read_sql_query(sql_query, conn)
            return df
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return pd.DataFrame()

    def query(self, sql_query: str) -> list[tuple]:
        """Execute an SQL query and return the result as a list of tuples.

        Args:
            sql_query (str): The SQL query to execute

        Returns:
            list[tuple]: List of tuples containing the query results
        """
        try:
            with connect(db_path) as conn:
                cursor = conn.cursor()
                result = cursor.execute(sql_query).fetchall()
            return result
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

# Leave this code unchanged
def query(func):
    """
    Decorator that runs a standard sql execution
    and returns a list of tuples
    """
    @wraps(func)
    def run_query(*args, **kwargs):
        query_string = func(*args, **kwargs)
        connection = connect(db_path)
        cursor = connection.cursor()
        result = cursor.execute(query_string).fetchall()
        connection.close()
        return result
    return run_query
