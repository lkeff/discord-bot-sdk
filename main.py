from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os
import discord

# @NOTE: may be we should create a class for bot?
bot = discord.Bot(intents=discord.Intents.all())
bot.run(os.getenv('BOT_TOKEN'))