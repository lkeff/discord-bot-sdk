from dotenv import load_dotenv, find_dotenv  # we need to import dotenv before os
load_dotenv(find_dotenv())

import os
import discord
from config import globals


if __name__ == '__main__':
    globals.ABS_PATH = os.path.dirname(os.path.abspath(__file__))

    cogs_list = [cog.replace('.py', '') 
                 for cog in os.listdir(os.path.join(globals.ABS_PATH, 'cogs')) 
                 if cog.endswith('.py')]

    bot = discord.Bot(intents=discord.Intents.all())  # Bot initialization
    globals.BOT = bot                                 # BOT - global variable, bot - local

    for cog in cogs_list:                             # For file ends with .py in /cogs/ folder
        bot.load_extension(f'cogs.{cog}')             # Load cog

    bot.run(os.getenv('BOT_TOKEN'))                   # Run with token from .env (or smth)