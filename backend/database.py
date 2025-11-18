"""
Database connection and utility functions
Provides database connection pool and helper functions for queries
"""

import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from config import get_settings

settings = get_settings()

# Database connection pool for better performance
connection_pool = None

def init_connection_pool():
    """Initialize the database connection pool"""
    global connection_pool
    try:
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            1, 20,  # min and max connections
            host=settings.db_host,
            port=settings.db_port,
            user=settings.db_user,
            password=settings.db_password,
            database=settings.db_name
        )
        print("✓ Database connection pool initialized")
    except Exception as e:
        print(f"✗ Error initializing connection pool: {e}")
        raise

@contextmanager
def get_db_connection():
    """
    Context manager for database connections
    Automatically returns connection to pool after use
    """
    connection = None
    try:
        connection = connection_pool.getconn()
        yield connection
    finally:
        if connection:
            connection_pool.putconn(connection)

@contextmanager
def get_db_cursor(commit=False):
    """
    Context manager for database cursors with RealDictCursor
    Returns results as dictionaries for easier JSON serialization
    """
    with get_db_connection() as connection:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        try:
            yield cursor
            if commit:
                connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()

def close_connection_pool():
    """Close all connections in the pool"""
    global connection_pool
    if connection_pool:
        connection_pool.closeall()
        print("✓ Database connection pool closed")
