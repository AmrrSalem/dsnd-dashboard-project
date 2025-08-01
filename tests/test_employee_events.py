import pytest
from pathlib import Path

# Using pathlib create a project_root variable set to the absolute path
# for the root of this project
project_root = Path(__file__).parent.absolute()

# Apply the pytest fixture decorator to a db_path function
@pytest.fixture
def db_path():
    """Provide the path to the employee_events.db file.

    Returns:
        Path: Pathlib object pointing to employee_events.db
    """
    # Using the project_root variable, return a pathlib object for employee_events.db
    return project_root / "employee_events.db"

# Define a function called test_db_exists
def test_db_exists(db_path):
    """Test that the employee_events.db file exists.

    Args:
        db_path (Path): Path to the employee_events.db file
    """
    # Using the pathlib .is_file method, assert that the database file exists
    assert db_path.is_file(), f"Database file not found at {db_path}"

# Provided fixtures (unchanged)
@pytest.fixture
def db_conn(db_path):
    from sqlite3 import connect
    return connect(db_path)

@pytest.fixture
def table_names(db_conn):
    name_tuples = db_conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    return [x[0] for x in name_tuples]

# Define a test function called test_employee_table_exists
def test_employee_table_exists(table_names):
    """Test that the 'employee' table exists in the database.

    Args:
        table_names (list): List of table names in the database
    """
    # Assert that the string 'employee' is in the table_names list
    assert 'employee' in table_names, "'employee' table not found in database"

# Define a test function called test_team_table_exists
def test_team_table_exists(table_names):
    """Test that the 'team' table exists in the database.

    Args:
        table_names (list): List of table names in the database
    """
    # Assert that the string 'team' is in the table_names list
    assert 'team' in table_names, "'team' table not found in database"

# Define a test function called test_employee_events_table_exists
def test_employee_events_table_exists(table_names):
    """Test that the 'employee_events' table exists in the database.

    Args:
        table_names (list): List of table names in the database
    """
    # Assert that the string 'employee_events' is in the table_names list
    assert 'employee_events' in table_names, "'employee_events' table not found in database"
