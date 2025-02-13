import sqlite3
import os
from logging_module import setup_logger

# Initialize logger
logger = setup_logger(log_dir="logs", logger_name="Database_Setup")
logger.info("Starting database setup...")

# Database path
db_path = "bot_data.db"
logger.info(f"Connecting to SQLite database: {db_path}")

# Connect to SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
logger.info("Database connection established.")

# Create messages table if it doesn't exist
logger.info("Ensuring messages table exists...")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        user_id TEXT,
        message TEXT,
        channel_id TEXT,
        timestamp TEXT
    )
''')
conn.commit()
logger.info("Database setup complete.")

# Close the connection
conn.close()
logger.info("Database connection closed.")
