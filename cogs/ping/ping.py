import os
import json

import discord
from discord.ext import commands

from localization.locales import Locales, _


class Ping(commands.Cog):

    def __init__(self, bot):
        self.bot: discord.Bot = bot
        
        # If want to override any localization only inside current cog
        # or if you want to add extra localizations for current cog
        # you should use this construction        
        cog_path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(cog_path, 'ping_locales.json'), 'r', encoding='utf-8') as file:
            self.cog_locales = json.load(file)

    @discord.slash_command(
        name='ping',                                  # default command name
        description='Default ping!',                  # default command description
        **Locales().localize_command('ping_command')  # get ping_command name, description translation for ru and en-GB
    )
    async def ping_command(self, ctx: discord.ApplicationContext):
        await ctx.respond(_('Hello, my dear {}!', ctx.user.name) + ' ' + _('Ping: {}', round(self.bot.latency, 2)))


def setup(bot):
    bot.add_cog(Ping(bot))