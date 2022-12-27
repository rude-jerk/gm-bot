import os

from dotenv import load_dotenv

load_dotenv()

LOG_NAME = 'gm_bot'

BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
SERVER_ID = os.getenv('DISCORD_SERVER_ID')
LOG_CHANNEL_ID = os.getenv('DISCORD_LOG_CHANNEL')

DATABASE_HOST = os.getenv('DB_HOST')
DATABASE_PORT = os.getenv('DB_PORT')
DATABASE_NAME = os.getenv('DB_NAME')
DATABASE_USER = os.getenv('DB_USER')
DATABASE_PASS = os.getenv('DB_PASS')

if not BOT_TOKEN:
    raise Exception('Missing environmental variable: DISCORD_BOT_TOKEN')

if not SERVER_ID:
    raise Exception('Missing environment variable: DISCORD_SERVER_ID')
