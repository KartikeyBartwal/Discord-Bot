import discord
import sqlite3
import os
from dotenv import load_dotenv
from logging_module import setup_logger

# Initialize logger
logger = setup_logger(log_dir="logs", logger_name="Discord_Bot")
logger.info("Starting Discord bot...")

# Load environment variables from .env file
load_dotenv()
logger.info("Loaded environment variables.")

# Get bot token
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    logger.critical("BOT_TOKEN is missing. Ensure it's set in the .env file.")
    exit(1)

# Set up bot intents
intents = discord.Intents.default()
intents.message_content = True  # Allows reading message content
logger.info("Bot intents configured.")

# Initialize bot client
client = discord.Client(intents=intents)
logger.info("Discord client initialized.")

# Connect to SQLite database (or create it if it doesn't exist)
db_path = "bot_data.db"
logger.info(f"Connecting to SQLite database: {db_path}")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
logger.info("Database connection established.")

# Create a table for storing messages
logger.info("Creating messages table if not exists...")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        message TEXT,
        timestamp TEXT
    )
''')
conn.commit()
logger.info("Database table setup complete.")

@client.event
async def on_ready():
    logger.info(f'✅ Bot is online as {client.user}')
    print(f'✅ Bot is online as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        logger.debug("Ignoring bot's own message.")
        return  # Ignore the bot's own messages

    logger.info(f"📩 Message received from {message.author}: {message.content}")
    
    # Log message details in SQLite database
    try:
        cursor.execute("INSERT INTO messages (user, user_id, message, channel_id, timestamp) VALUES (?, ?, ?, ?, ?)",
               (message.author.name, str(message.author.id), message.content, str(message.channel.id), str(message.created_at)))
        conn.commit()
        logger.info("Message logged to database successfully.")
    except Exception as e:
        logger.error(f"Failed to log message to database: {e}")

client.run(TOKEN)