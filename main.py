from dotenv import load_dotenv, find_dotenv  # we need to import dotenv before os
load_dotenv(find_dotenv())

import os
import discord
from config import globals


def load_cogs(bot: discord.Bot):
    """Cogs can be contained only in 1 extra folder.
    Example: cogs/global_events.py, cogs/ping/ping.py
    This file won't be loaded: cogs/foo/bar/viewer.py"""
    cogs = []
    files_in_cogs_folder = os.listdir(os.path.join(globals.ABS_PATH, 'cogs'))

    folders = ['']
    folders.extend([file
                    for file in files_in_cogs_folder
                    if os.path.isdir(os.path.join(globals.ABS_PATH, 'cogs', file))])
    
    for folder in folders:
        cogs.extend([f"cogs.{folder + '.' if folder else ''}{cog.replace('.py', '')}" 
                    for cog in os.listdir(os.path.join(globals.ABS_PATH, 'cogs', folder)) 
                    if cog.endswith('.py')])

    for cog in cogs:
        bot.load_extension(cog)


def main():
    globals.ABS_PATH = os.path.abspath(os.getcwd())    

    bot = discord.Bot(intents=discord.Intents.all())
    globals.BOT = bot

    load_cogs(bot)
    bot.run(os.getenv('BOT_TOKEN'))


if __name__ == '__main__':
    main()