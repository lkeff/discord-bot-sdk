from dotenv import load_dotenv, find_dotenv  # we need to import dotenv before os
load_dotenv(find_dotenv())

import os
import sys
import discord
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))
import globals


def load_cogs(bot: discord.Bot):
    """Cogs can be contained only in 1 extra folder.
    Example: cogs/global_events.py, cogs/ping/ping.py, cogs/game/game.py
    This file won't be loaded: cogs/foo/bar/viewer.py"""
    cogs = []
    files_in_cogs_folder = os.listdir(os.path.join(globals.ABS_PATH, 'cogs'))

    folders = ['']
    folders.extend([file
                    for file in files_in_cogs_folder
                    if os.path.isdir(os.path.join(globals.ABS_PATH, 'cogs', file))])

    # Always include 'game' folder for new mini-mods
    if 'game' not in folders:
        folders.append('game')

    # Always include calm_guard for moderation
    if 'calm_guard.py' not in files_in_cogs_folder:
        raise FileNotFoundError("calm_guard.py cog is missing in cogs directory!")
    cogs.append('cogs.calm_guard')

    for folder in folders:
        cogs.extend([f"cogs.{folder + '.' if folder else ''}{cog.replace('.py', '')}"
                    for cog in os.listdir(os.path.join(globals.ABS_PATH, 'cogs', folder))
                    if cog.endswith('.py') and cog != 'calm_guard.py'])

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