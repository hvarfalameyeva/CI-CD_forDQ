"""
Connects to a SQL database using pyodbc
"""
import pyodbc
import pytest


# Fixture to build connection to DB
@pytest.fixture
def db_connection():
    SERVER = r"EPBYBREW012E\SQLEXPRESS"
    DATABASE = 'TRN'
    # creation of DB connection
    conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};'  f'Encrypt=no;Trusted_connection=yes')
    yield conn
    # Closure of the connection
    conn.close()


# Funtion to execute SQL queries
def get_data(query, conn):
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    return result


# Validate hr.departments does not contain NULL values in primary key column
def test_no_null_primary_key(db_connection):
    query = "SELECT COUNT(*) FROM hr.departments WHERE department_id IS NULL"
    result = get_data(query, db_connection)
    expected_count = 0
    assert result[0] == expected_count, f"Expected {expected_count} but got {result[0]}"

# Validate hr.employees does not contain NULL values in primary key column
def test_no_null_primary_key(db_connection):
    query = "SELECT COUNT(*) FROM  hr.employees WHERE employee_id IS NULL"
    result = get_data(query, db_connection)
    expected_count = 0
    assert result[0] == expected_count, f"Expected {expected_count} but got {result[0]}"

# Validate hr.departments does not contain duplicates in primary key column
def test_no_duplicate_primary_key(db_connection):
    query = "SELECT department_id, COUNT(*) FROM hr.departments GROUP BY department_id HAVING COUNT(*) > 1"
    result = get_data(query, db_connection)
    assert result is None, f"Expected no duplicates but got {result}"


# Validate hr.employees table does not contain invalid email formats in email column
def test_no_invalid_email_formats (db_connection):
    query = "SELECT COUNT(email) FROM hr.employees WHERE email not like '%@%.%'"
    result = get_data(query, db_connection)
    expected_count = 0
    assert result[0] == expected_count, f"Expected no duplicates but got {result}"


# Validate hr.employees table does not contain invalid hire date in the future
def test_no_invalid_hire_dates (db_connection):
    query = "SELECT employee_id FROM hr.employees WHERE hire_date > GETDATE()"
    result = get_data(query, db_connection)
    assert result is None, f"Expected no duplicates but got {result}"


# Validate hr.locations table does not contain invalid country_id (secondary key)
def test_no_invalid_country_id (db_connection):
    query = "SELECT location_id FROM hr.locations WHERE country_id not in (SELECT country_id FROM hr.countries)"
    result = get_data(query, db_connection)
    assert result is None, f"Expected no duplicates but got {result}"


# Validate hr.jobs table has valid values in max_salary and min_salary columns
def test_no_invalid_salary (db_connection):
    query = "SELECT job_id FROM hr.jobs WHERE max_salary < min_salary"
    result = get_data(query, db_connection)
    assert result is None, f"Expected no duplicates but got {result}"