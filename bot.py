import logging
from logging.handlers import RotatingFileHandler
from os.path import join, dirname

from disnake import Intents
from disnake.ext import commands
from disnake.ext.commands import errors
from mysql.connector import pooling as mysql

import settings

this_dir = dirname(__file__)
logger = logging.getLogger(settings.LOG_NAME)
logger.setLevel(logging.INFO)

if not len(logger.handlers):
    handler = RotatingFileHandler(filename=join(this_dir, 'logs/gm.log'), encoding='utf-8', mode='w', maxBytes=50000,
                                  backupCount=5)
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

intents = Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents, sync_commands_debug=True)


@bot.event
async def on_ready():
    bot.db_pool = mysql.MySQLConnectionPool(
        pool_name='discord_bot',
        pool_size=5,
        pool_reset_session=False,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
        database=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASS
    )

    bot.gm_server = bot.get_guild(int(settings.SERVER_ID))
    if not bot.gm_server:
        raise Exception('Unable to locate GM discord server.')
    bot.log_channel = bot.get_channel(int(settings.LOG_CHANNEL_ID))
    if not bot.log_channel:
        logger.warning("Unable to locate log channel, command usage will not be logged.")


@bot.event
async def on_slash_command_error(inter, error):
    if isinstance(error, errors.MissingRole):
        await inter.send('You do not have the required role to use this command!', ephemeral=True)


if __name__ == '__main__':
    bot.load_extension('cogs.transactions')
    bot.run(token=settings.BOT_TOKEN)
