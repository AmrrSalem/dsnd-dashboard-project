import pandas as pd
import sqlite3
from typing import List
from abc import ABC, abstractmethod


class QueryBase(ABC):
    """Base class for querying employee_events database tables.

    This abstract base class provides common methods for querying
    employee-related event data from different tables.
    """
    name: str = ""

    def __init__(self, db_path: str):
        """Initialize QueryBase with database connection path.

        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path

    def names(self) -> List[str]:
        """Return a list of names from the table.

        Returns:
            List[str]: Empty list as placeholder for names
        """
        return []

    def event_counts(self, id: int) -> pd.DataFrame:
        """Query event counts grouped by date for a specific ID.

        Args:
            id (int): The ID to filter events

        Returns:
            pd.DataFrame: DataFrame containing event dates and counts
        """
        query = f"""
            SELECT 
                event_date,
                SUM(CASE WHEN event_type = 'positive' THEN 1 ELSE 0 END) as positive_events,
                SUM(CASE WHEN event_type = 'negative' THEN 1 ELSE 0 END) as negative_events
            FROM {self.name}
            WHERE employee_id = {id}
            GROUP BY event_date
            ORDER BY event_date
        """

        try:
            with sqlite3.connect(self.db_path) as conn:
                df = pd.read_sql_query(query, conn)
            return df
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return pd.DataFrame()

    def notes(self, id: int) -> pd.DataFrame:
        """Query notes for a specific ID.

        Args:
            id (int): The ID to filter notes

        Returns:
            pd.DataFrame: DataFrame containing note dates and notes
        """
        query = f"""
            SELECT 
                note_date,
                note
            FROM notes
            WHERE employee_id = {id}
            AND table_name = '{self.name}'
            ORDER BY note_date
        """

        try:
            with sqlite3.connect(self.db_path) as conn:
                df = pd.read_sql_query(query, conn)
            return df
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return pd.DataFrame()


# Example implementation of a derived class
class EmployeeEvents(QueryBase):
    """Concrete class for querying employee events."""
    name = "employee_events"

    def names(self) -> List[str]:
        """Return a list of employee names.

        Returns:
            List[str]: List of employee names from the table
        """
        query = f"""
            SELECT DISTINCT employee_name
            FROM {self.name}
        """

        try:
            with sqlite3.connect(self.db_path) as conn:
                df = pd.read_sql_query(query, conn)
                return df['employee_name'].tolist()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
