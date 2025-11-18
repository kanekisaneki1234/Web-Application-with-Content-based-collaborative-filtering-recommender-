"""
Database initialization script
This script creates the database schema and populates it with sample data
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'user': os.getenv('DB_USER', 'anime_user'),
    'password': os.getenv('DB_PASSWORD', 'anime_password'),
    'database': os.getenv('DB_NAME', 'anime_db')
}

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server (not to a specific database)
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database='postgres'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (DB_CONFIG['database'],)
        )

        if not cursor.fetchone():
            cursor.execute(f"CREATE DATABASE {DB_CONFIG['database']}")
            print(f"✓ Database '{DB_CONFIG['database']}' created successfully")
        else:
            print(f"✓ Database '{DB_CONFIG['database']}' already exists")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"✗ Error creating database: {e}")
        raise

def run_sql_file(cursor, filepath):
    """Execute SQL commands from a file"""
    try:
        with open(filepath, 'r') as f:
            sql = f.read()
            cursor.execute(sql)
        print(f"✓ Successfully executed {os.path.basename(filepath)}")
    except Exception as e:
        print(f"✗ Error executing {filepath}: {e}")
        raise

def initialize_database():
    """Initialize the database with schema and sample data"""
    try:
        # Connect to the anime database
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        print("\n🗄️  Initializing database schema...")
        run_sql_file(cursor, 'database/schema.sql')

        print("\n📊 Populating database with sample data...")
        run_sql_file(cursor, 'database/seed_data.sql')

        # Commit changes
        conn.commit()

        # Verify data
        cursor.execute("SELECT COUNT(*) FROM anime")
        count = cursor.fetchone()[0]
        print(f"\n✓ Database initialized successfully with {count} anime entries")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        raise

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Anime Database Initialization")
    print("=" * 60)

    try:
        create_database()
        initialize_database()
        print("\n" + "=" * 60)
        print("✅ Database setup completed successfully!")
        print("=" * 60)
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ Database setup failed!")
        print("=" * 60)
        exit(1)
