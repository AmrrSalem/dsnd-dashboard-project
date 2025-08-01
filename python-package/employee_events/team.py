# Import the QueryBase class
from query_base import QueryBase  # Assuming QueryBase is in query_base.py

# Import dependencies for sql execution
from sql_execution import execute_sql  # Hypothetical module for SQL execution
import pandas as pd
import sqlite3
from typing import List, Tuple


class Team(QueryBase):
    """Subclass of QueryBase for querying team table.

    Provides methods to query team-specific data from the team table
    in the employee_events database.
    """
    name: str = "team"

    def names(self) -> List[Tuple[str, int]]:
        """Retrieve team names and IDs of all teams.

        Returns:
            List[Tuple[str, int]]: List of tuples containing team name and ID
        """
        # Query 5
        query = """
            SELECT team_name, team_id
            FROM team
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
        """Retrieve team name for a specific team ID.

        Args:
            id (int): The team ID to filter by

        Returns:
            List[Tuple[str]]: List of tuples containing the team name
        """
        # Query 6
        query = f"""
            SELECT team_name
            FROM {self.name}
            WHERE team_id = {id}
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
            id (int): The team ID to filter by

        Returns:
            pd.DataFrame: DataFrame containing positive and negative event sums
        """
        query = f"""
            SELECT positive_events, negative_events FROM (
                SELECT employee_id
                     , SUM(positive_events) positive_events
                     , SUM(negative_events) negative_events
                FROM {self.name}
                JOIN employee_events
                    USING(team_id)
                WHERE {self.name}.team_id = {id}
                GROUP BY employee_id
            )
        """

        try:
            with sqlite3.connect(self.db_path) as conn:
                df = pd.read_sql_query(query, conn)
            return df
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return pd.DataFrame()
